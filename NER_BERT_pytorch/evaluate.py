"""Evaluate the model"""

import argparse
import random
import logging
import os
import time

import numpy as np
import torch

from pytorch_pretrained_bert import BertForTokenClassification, BertConfig
#NER_BERT_pytorch
from .metrics import f1_score
from .metrics import classification_report

from .data_loader import DataLoader
from .utils import Params, RunningAverage, set_logger, load_checkpoint


# parser = argparse.ArgumentParser()
# parser.add_argument('--data_dir', default='data/msra/', help="Directory containing the dataset")
# parser.add_argument('--bert_model_dir', default='bert-base-chinese-pytorch', help="Directory containing the BERT model in PyTorch")
# parser.add_argument('--model_dir', default='experiments/base_model', help="Directory containing params.json")
# parser.add_argument('--seed', type=int, default=23, help="random seed for initialization")
# parser.add_argument('--restore_file', default='best', help="name of the file in `model_dir` containing weights to load")
# parser.add_argument('--multi_gpu', default=False, action='store_true', help="Whether to use multiple GPUs if available")
# parser.add_argument('--fp16', default=False, action='store_true', help="Whether to use 16-bit float precision instead of 32-bit")


def evaluate(model, data_iterator, params, mark='Eval', verbose=False):
    """Evaluate the model on `steps` batches."""
    # set model to evaluation mode
    model.eval()

    idx2tag = params.idx2tag

    true_tags = []
    pred_tags = []

    # a running average object for loss
    loss_avg = RunningAverage()

    for _ in range(params.eval_steps):
    # while True:
        # fetch the next evaluation batch
        # print('Hi')
        try:
            batch_data, batch_tags = next(data_iterator)
        except Exception as e:
            break
        batch_masks = batch_data.gt(0)

        # loss = model(batch_data, token_type_ids=None, attention_mask=batch_masks, labels=batch_tags)
        # if params.n_gpu > 1 and params.multi_gpu:
        #     loss = loss.mean()
        # loss_avg.update(loss.item())
        
        batch_output = model(batch_data, token_type_ids=None, attention_mask=batch_masks)  # shape: (batch_size, max_len, num_labels)
        
        batch_output = batch_output.detach().cpu().numpy()
        batch_tags = batch_tags.to('cpu').numpy()

        pred_tags.extend([idx2tag.get(idx) for indices in np.argmax(batch_output, axis=2) for idx in indices])
        true_tags.extend([idx2tag.get(idx) for indices in batch_tags for idx in indices])
        
    # assert len(pred_tags) == len(true_tags)
    # print(pred_tags)
    # print(len(pred_tags))

    # logging loss, f1 and report
    # metrics = {}
    # f1 = f1_score(true_tags, pred_tags)
    # metrics['loss'] = loss_avg()
    # metrics['f1'] = f1
    # metrics_str = "; ".join("{}: {:05.2f}".format(k, v) for k, v in metrics.items())
    # logging.info("- {} metrics: ".format(mark) + metrics_str)

    # if verbose:
    #     report = classification_report(true_tags, pred_tags)
    #     logging.info(report)

    # return metrics
    return pred_tags


# RUN THIS FIRST
def evaluate_config():

    # args = parser.parse_args()
    data_dir = '/home/deepracer/DeepRacer/AI_Samurai/Esun_AML/NER_BERT_pytorch/temp'
    bert_model_dir = '/home/deepracer/DeepRacer/AI_Samurai/Esun_AML/NER_BERT_pytorch/bert-base-chinese-pytorch'
    model_dir = '/home/deepracer/DeepRacer/AI_Samurai/Esun_AML/NER_BERT_pytorch/experiments/base_model'

    seed = 23 # help="random seed for initialization"
    restore_file = 'best' # help="name of the file in `model_dir` containing weights to load"
    multi_gpu = False # action='store_true', help="Whether to use multiple GPUs if available"
    fp16 = False # action='store_true', help="Whether to use 16-bit float precision instead of 32-bit"

    # Load the parameters from json file
    json_path = os.path.join(model_dir, 'params.json')
    assert os.path.isfile(json_path), "No json configuration file found at {}".format(json_path)
    params = Params(json_path)

    # Use GPUs if available
    params.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    params.n_gpu = torch.cuda.device_count()
    params.multi_gpu = multi_gpu

    # Set the random seed for reproducible experiments
    random.seed(seed)
    torch.manual_seed(seed)
    if params.n_gpu > 0:
        torch.cuda.manual_seed_all(seed)  # set random seed for all GPUs
    params.seed = seed

    # Set the logger
    set_logger(os.path.join(model_dir, 'evaluate.log'))

    # Create the input data pipeline
    logging.info("Loading the dataset...")

    # Initialize the DataLoader
    data_loader = DataLoader(data_dir, bert_model_dir, params, token_pad_idx=0)

    
    logging.info("- done.")

    # Define the model
    config_path = os.path.join(bert_model_dir, 'bert_config.json')
    config = BertConfig.from_json_file(config_path)
    model = BertForTokenClassification(config, num_labels=len(params.tag2idx))

    model.to(params.device)
    # Reload weights from the saved file
    load_checkpoint(os.path.join(model_dir, restore_file + '.pth.tar'), model)
    if fp16:
        model.half()
    if params.n_gpu > 1 and multi_gpu:
        model = torch.nn.DataParallel(model)

    return data_loader, model, params


if __name__ == '__main__':

    data_loader, model, params = evaluate_config()

    # Load data
    test_data = data_loader.load_data('test')

    # Specify the test set size
    params.test_size = test_data['size']
    params.eval_steps = params.test_size // params.batch_size
    # params.eval_steps = params.test_size
    test_data_iterator = data_loader.data_iterator(test_data, shuffle=False)

    logging.info("Starting evaluation...")
    
    test_metrics = evaluate(model, test_data_iterator, params, mark='Test', verbose=True)
    
import torch
import os
from collections import OrderedDict
from tqdm import tqdm
from tensorboardX import SummaryWriter
import argparse
from dataset import get_dataloader
from common import get_config
from utils import cycle
from agent import get_agent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--continue', dest='continue_path', type=str, required=False)
    parser.add_argument('-g', '--gpu_ids', type=int, default=0, required=False, help="specify gpu ids")
    parser.add_argument('--vis', action='store_true', default=False, help="visualize output in training")
    args = parser.parse_args()

    # create experiment config
    config = get_config(stage)
    os.environ["CUDA_VISIBLE_DEVICES"] = str(args.gpu_ids)
    config.device = torch.device("cuda:0")
    print(config)

    # create soft link to experiment log directory
    if not os.path.exists('train_log'):
        os.symlink(config.exp_dir, 'train_log')

    # create network and training agent
    tr_agent = get_agent(config)

    # load from checkpoint if provided
    if args.continue_path:
        tr_agent.load_ckpt(args.continue_path)

    print(tr_agent.net)

    # create tensorboard writer
    train_tb = SummaryWriter(os.path.join(config.log_dir, 'train.events'))
    val_tb = SummaryWriter(os.path.join(config.log_dir, 'val.events'))

    # create dataloader
    train_loader = get_dataloader('train', batch_size=config.batch_size, num_workers=config.num_workers)
    val_loader = get_dataloader('validation', batch_size=config.batch_size, num_workers=config.num_workers)
    val_loader = cycle(val_loader)

    # start training
    clock = tr_agent.clock

    for e in range(clock.epoch, config.nr_epochs):
        # begin iteration
        pbar = tqdm(train_loader)
        for b, data in enumerate(pbar):
            # train step
            outputs, losses = tr_agent.train_func(data)

            losses_values = {k:v.item() for k, v in losses.items()}

            # record loss to tensorboard
            for k, v in losses_values.items():
                train_tb.add_scalar(k, v, clock.step)

            # visualize
            if args.vis and clock.step % config.visualize_frequency == 0:
                pass
                # with torch.no_grad():
                #     tr_agent.visualize_batch(data['path'][0], train_tb)

            pbar.set_description("EPOCH[{}][{}]".format(e, b))
            pbar.set_postfix(OrderedDict(losses_values))

            # validation step
            if clock.step % config.val_frequency == 0:
                data = next(val_loader)

                outputs, losses = tr_agent.val_func(data)

                losses_values = {k: v.item() for k, v in losses.items()}

                for k, v in losses_values.items():
                    val_tb.add_scalar(k, v, clock.step)

                if args.vis and clock.step % config.visualize_frequency == 0:
                    pass 
                    # with torch.no_grad():
                    #     tr_agent.visualize_batch(data['path'][0], val_tb)

            clock.tick()

        train_tb.add_scalar('learning_rate', tr_agent.optimizer.param_groups[-1]['lr'], clock.epoch)
        tr_agent.update_learning_rate()

        clock.tock()

        if clock.epoch % config.save_frequency == 0:
            tr_agent.save_ckpt()
        tr_agent.save_ckpt('latest.pth.tar')


if __name__ == '__main__':
    main()

from collections import OrderedDict
from tqdm import tqdm
import argparse
from dataset import get_dataloader
from common import get_config
from utils import cycle
from agent import get_agent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--continue', dest='cont',  action='store_true', help="continue training from checkpoint")
    parser.add_argument('--ckpt', type=str, default='latest', required=False, help="desired checkpoint to restore")
    parser.add_argument('-g', '--gpu_ids', type=int, default=0, required=False, help="specify gpu ids")
    parser.add_argument('--vis', action='store_true', default=False, help="visualize output in training")
    args = parser.parse_args()

    # create experiment config
    config = get_config(args)
    print(config)

    # create network and training agent
    tr_agent = get_agent(config)
    print(tr_agent.net)

    # load from checkpoint if provided
    if args.cont:
        tr_agent.load_ckpt(args.ckpt)

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

            # visualize
            if args.vis and clock.step % config.visualize_frequency == 0:
                pass
                # with torch.no_grad():
                #     tr_agent.visualize_batch(data['path'][0], train_tb)

            pbar.set_description("EPOCH[{}][{}]".format(e, b))
            pbar.set_postfix(OrderedDict({k: v.item() for k, v in losses.items()}))

            # validation step
            if clock.step % config.val_frequency == 0:
                data = next(val_loader)
                outputs, losses = tr_agent.val_func(data)

                if args.vis and clock.step % config.visualize_frequency == 0:
                    pass
                    # with torch.no_grad():
                    #     tr_agent.visualize_batch(data['path'][0], val_tb)

            clock.tick()

        tr_agent.update_learning_rate()
        clock.tock()

        if clock.epoch % config.save_frequency == 0:
            tr_agent.save_ckpt()
        tr_agent.save_ckpt('latest')


if __name__ == '__main__':
    main()

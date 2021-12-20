from collections import OrderedDict
from tqdm import tqdm
from dataset import get_dataloader
from common import get_config
from utils import cycle
from agent import get_agent


def main():
    # create experiment config containing all hyperparameters
    config = get_config('train')

    # create network and training agent
    tr_agent = get_agent(config)

    # load from checkpoint if provided
    if config.cont:
        tr_agent.load_ckpt(config.ckpt)

    # create dataloader
    train_loader = get_dataloader('train', config)
    val_loader = get_dataloader('validation', config)
    val_loader = cycle(val_loader)

    # start training
    clock = tr_agent.clock

    for e in range(clock.epoch, config.n_epochs):
        # begin iteration
        pbar = tqdm(train_loader)
        for b, data in enumerate(pbar):
            # train step
            outputs, losses = tr_agent.train_func(data)

            # visualize
            if config.vis_frequency is not None and clock.step % config.vis_frequency == 0:
                tr_agent.visualize_batch(data, "train", outputs=outputs)

            pbar.set_description("EPOCH[{}][{}]".format(e, b))
            pbar.set_postfix(OrderedDict({k: v.item() for k, v in losses.items()}))

            # validation step
            if clock.step % config.val_frequency == 0:
                data = next(val_loader)
                outputs, losses = tr_agent.val_func(data)

                if config.vis_frequency is not None and clock.step % config.vis_frequency == 0:
                    tr_agent.visualize_batch(data, "validation", outputs=outputs)

            clock.tick()

        tr_agent.update_learning_rate()
        clock.tock()

        if clock.epoch % config.save_frequency == 0:
            tr_agent.save_ckpt()
        tr_agent.save_ckpt('latest')


if __name__ == '__main__':
    main()

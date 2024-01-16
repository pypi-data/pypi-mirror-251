import torchinfo


def visualize(model):
    print(torchinfo.summary(model))


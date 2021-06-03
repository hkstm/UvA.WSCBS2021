#!/usr/bin/env python3
from matplotlib import pyplot as plt
import yaml

if __name__ == "__main__":
    plt.plot([2,3,1,4])
    plt.savefig('/data/fig.png')
    print(yaml.dump({"output": "ok"}))

# A ~~fake~~ simple display manager
![image](https://github.com/thiagolopes/dialog_xsessions/assets/5994972/e95da4a2-ee9d-4351-86e9-1360cb2344b3)

## About
This script does not currently function as a complete display manager (yet). Its purpose is to list all available display managers on your system, X and Wayland.

## Run
You can use in your `.bashrc`|`.zshrc` to run when log to TTY1
```sh
if [[ -z "$DISPLAY" ]] && [[ $(tty) = /dev/tty1 ]]; then
    DP_PATH="$(python ~/.display_manager.py)"
    echo "Executing: $DP_PATH"
    eval "$DP_PATH"
fi
```

- python 3.10>=
- dialog

References:
[What is a Display Manager?](https://freedesktop.org/wiki/Software/LightDM/Design/)


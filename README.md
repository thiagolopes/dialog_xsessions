# A ~~fake~~ simple display manager
![image](https://github.com/thiagolopes/dialog_xsessions/assets/5994972/e95da4a2-ee9d-4351-86e9-1360cb2344b3)

## About
This is script is not a complete display manager, working together with systemd and manage user logging.
The only function of this script is return a valid desktop environment to be executed;

Wayland support soon.

## Run
You can use in your `.bashrc`|`.zshrc` to run when log to TTY1
```sh
if [[ -z "$DISPLAY" ]] && [[ $(tty) = /dev/tty1 ]]; then
    DP_PATH="$(python ~/.display_manager.py)"
    echo "Executing: $DP_PATH"
    eval "$DP_PATH"
fi
```

Do not need any external dependency.


References:
[What is a Display Manager?](https://freedesktop.org/wiki/Software/LightDM/Design/)

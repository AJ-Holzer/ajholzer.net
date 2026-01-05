# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


import threading
import subprocess
import time


def restart_api(delay: int) -> None:
    """Runs the restart script located at '/var/www/html/api.ajholzer.net_restart.sh' with the specified delay.

    Args:
        delay (int): The time to wait before restarting the process in seconds.
    """

    def restart() -> None:
        # Wait a few seconds to ensure everything is done
        time.sleep(delay)

        # Run restart script
        subprocess.run(
            ["sudo", "/var/www/html/api.ajholzer.net_restart.sh"],
            check=True,
        )

    threading.Thread(target=restart, daemon=True).start()

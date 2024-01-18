# User guide and documentation

## What can you do with the Python SDK?

1. You can use the Python SDK to search for the device.
2. You can use the Python SDK to connect and record data from the earbud.
3. You can download the data to your local machine.

---

## Prerequisites

- [Python 3.10](https://www.python.org/downloads/release/python-3100), if you already have another python version installed and you do not want to create a virtual environment to run the SDK, then you have to install Python 3.10 and [set it as your default Python](https://www.youtube.com/watch?v=zriWqGNJg4k).
  - If you have conflicts with other packages when installing the Python SDK:
    - Use [Conda](https://www.anaconda.com/products/distribution) which will create an environment and configure your python version to the correct one with the following command:
    ```bash
    conda create -n idun_env python=3.10
    ```
    or
    - Use [Pipenv](https://pypi.org/project/pipenv/) which will create your virtual environment manually using the following command.
    ```bash
    pipenv install --python 3.10
    ```

---

## Quick installation guide

1. Create a new repository or folder
2. Open the terminal in the same folder location or direct to that location within an already open terminal. For Windows you can use command prompt or Anaconda prompt, and Mac OS you can use the terminal or Anaconda prompt.

3. First activate the virtual environment if you have created one by using the following command, this command must always be run before using the python SDK:

   ```bash
   conda activate idun_env
   ```

   or

   ```bash
   pipenv shell
   ```

4. After the environment is activated, install the Python SDK using the following command:

   - With a [conda environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) use the following command:

   ```bash
   pip install idun-guardian-client
   ```

   or

   - With a [pipenv environment](https://pypi.org/project/pipenv/) use the following command:

   ```bash
   pipenv install idun-guardian-client
   ```

5. After installing the package, make sure that the dependencies are correctly installed by running the following command and inspecting the packages installed in the terminal output:

   ```bash
   pip list
   ```

---

## How to use the Python SDK

You can also download all the SDK example files from our [GitHub repository](https://github.com/iduntech/idun-guardian-client-examples.git), or copy and paste it from the examples below.

### Example 1: Search for the device

1. Create a new file inside the folder where you created your environment and name it `search.py`
2. Open the terminal in the folder and activate your virtual environment using the steps from the [Quick installation guide](#quick-installation-guide).
3. Open the `search.py` file and copy the code from step 1 below.
4. Activate the virtual environment **only** if you have not already done so by using:

   ```bash
   conda activate idun_env
   ```

   or

   ```bash
   pipenv shell
   ```

5. Run the following command in the terminal to run the code after you have activate the enviroment:
   ```bash
   python search.py
   ```

#### Recommendation of steps to follow which is elaborated further below

1. Search for the device
2. Check the battery level
3. Check the impedance
4. Record data from the earbud
5. Download the data from the cloud using the recording ID

## Pre Recording

### **1. Search the earbud manually**

- To search for the earbud, you need to run the following command in your python shell or in your python script:

```python
import asyncio
from idun_guardian_client import GuardianClient

bci = GuardianClient()

device_address = asyncio.run(bci.search_device())
```

- Follow the steps in the terminal to search for the earbud with the name `IGEB`
- If there are more than one IGEB device in the area, you will be asked to select the device you want to connect to connect to, a list such as below will pop up in the terminal:

  - For Windows:

  ```bash
  ----- Available devices -----

  Index | Name | Address
  ----------------------------
  0     | IGEB | XX:XX:XX:XX:XX:XX
  1     | IGEB | XX:XX:XX:XX:XX:XX
  2     | IGEB | XX:XX:XX:XX:XX:XX
  ----------------------------
  ```

  - For Mac OS:

  ```bash
  ----- Available devices -----
  Index | Name | UUID
  ----------------------------
  0    | IGEB | XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
  1    | IGEB | XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
  2    | IGEB | XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
  ----------------------------
  ```

- Enter the index number of the device you want to connect to.

### **2. Check battery level**

- To read out the battery level, you need to run the following command in your python shell or in your python script:

```python
import asyncio
from idun_guardian_client import GuardianClient

bci = GuardianClient()
bci.address = asyncio.run(bci.search_device())

asyncio.run(bci.start_battery())
```

### **3. Check impedance values**

- To read out the impedance values, you need to run the following command in your python shell or in your python script:

```python
import asyncio
from idun_guardian_client import GuardianClient

IMPEDANCE_DURATION = 5  # duration of impedance measurement in seconds
MAINS_FREQUENCY_60Hz = False
# mains frequency in Hz (50 or 60), for Europe 50Hz, for US 60Hz


# Get device address
bci = GuardianClient()
bci.address = asyncio.run(bci.search_device())

# start a recording session
asyncio.run(
    bci.start_recording(
        recording_timer=IMPEDANCE_DURATION,
        mains_freq_60hz=MAINS_FREQUENCY_60Hz,
        impedance_measurement=True)
)
```

## Recording

### **4. Start a recording**

- To start a recording with a pre-defined timer (e.g. `100` in seconds), you need to run the following command in your python shell or in your python script:

```python
import asyncio
from idun_guardian_client import GuardianClient

EXPERIMENT: str = "Sleeping"
RECORDING_TIMER: int = 36000 # 10 hours in seconds
LED_SLEEP: bool = False
SENDING_TIMEOUT: float = 2 # No sending receipt time before interrupt
BI_DIRECTIONAL_TIMEOUT: float = 20 # No bi-directional data receiving before interrupt

# start a recording session
bci = GuardianClient()
bci.address = asyncio.run(bci.search_device())

# start a recording session
asyncio.run(
    bci.start_recording(
        recording_timer=RECORDING_TIMER,
        led_sleep=LED_SLEEP,
        experiment=EXPERIMENT,
        sending_timout=SENDING_TIMEOUT,
        bi_directional_receiving_timeout=BI_DIRECTIONAL_TIMEOUT,
    )
)

```

- To stop the recording, either wait for the timer to run out or interrupt the recording
  - with Mac OS enter the cancellation command in the terminal running the script, this would be `Ctrl+.` or `Ctrl+C`
  - with Windows enter the cancellation command in the terminal running the script, this would be `Ctrl+C` or `Ctrl+Shift+C`

## Post Recording

### **4. Get all recorded info**

- To download the data, you need to first get the list of all your recordings and choose the one you would like to download
- Run the following command in your python shell or in your python script:

```python
from idun_guardian_client.igeb_api import GuardianAPI

api = GuardianAPI()

# get a list of all recordings
recording_list = api.get_recordings_info_all(device_id = "XX-XX-XX-XX-XX-XX") # Device ID is derived from the MAC address of the earbud and in the log file

```

### **5. Get recording info**

- To list the information on a specific recording, you need to run the following command in your python shell or in your python script:

```python
from idun_guardian_client.igeb_api import GuardianAPI

api = GuardianAPI()

# get single recording
api.get_recording_info_by_id(
    device_id = "XX-XX-XX-XX-XX-XX",
    recording_id = "xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
)

```

### **5. Download recording**

- To download the data insert the `device_id` along with the `recording_id` and run the following command in your python shell or in your python script

```python
from idun_guardian_client.igeb_api import GuardianAPI

api = GuardianAPI()

# download recording
api.download_recording_by_id(
    device_id = "XX-XX-XX-XX-XX-XX",
    recording_id = "xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx"
)
# The info about th recording can be found in the log file
```

## Adding meta data to recording

### **6. Post New Metadata for a Recording**

- This example illustrates how to use create_metadata.py to post new metadata for a specific recording. This script will create a new metadata entry, and this metadata will be linked to a returned metadata ID.

```python
import asyncio
from idun_data_models import (
    Metadata_in,
)
from config import PASSWORD
from idun_guardian_client.igeb_metadata import MetadataClient

# Configuration
DEVICE_ID = "XX-XX-XX-XX-XX-XX"  # Replace with your device ID, e.g., "XX-XX-XX-XX-XX-XX"
RECORDING_ID = "xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx"  # Replace with your recording ID, e.g., "py-e852d8d6-9235-4b4b-95a9-7a30f1076f55"
DISPLAY_NAME = "test"  # Display name for the metadata
EXPERIMENT_NAME = "nap"  # Name of the experiment

# Initialize MetadataClient
client = MetadataClient(DEVICE_ID, RECORDING_ID, PASSWORD)

# Create Metadata
metadata_markers = asyncio.run(
    client.create_metadata(
        Metadata_in(
            displayName=DISPLAY_NAME,
            experiment_name=EXPERIMENT_NAME,
        ),
    )
)
```

### **7. Create Markers for a Recording**

- This example demonstrates how to use the create_markers.py script to add new markers to an existing metadata ID. The script creates new marker entries, which will be added to the specified metadata. Note: Before running this script, you should have already created metadata for the recording using create_metadata.py.

```python
import asyncio
import numpy as np
from datetime import datetime
from idun_data_models.rest_metadata import Marker
from config import PASSWORD
from idun_guardian_client.igeb_metadata import MetadataClient

# Configuration
META_DATA_ID = "19"  # Replace with your metadata ID
DEVICE_ID = "XX-XX-XX-XX-XX-XX"  # Replace with your device ID, e.g., "XX-XX-XX-XX-XX-XX"
RECORDING_ID = "xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx"  # Replace with your recording ID

# Generate Markers
MARKERS = [
    Marker(timestamp=datetime.now(), marker={"sleepy": np.random.randint(10)})
    for _ in range(100)
]

# Initialize MetadataClient
client = MetadataClient(DEVICE_ID, RECORDING_ID, PASSWORD)

# Create Markers
response = asyncio.run(client.create_markers(META_DATA_ID, MARKERS))

# Output Result
if response:
    print(
        f"Successfully added markers to the metadata ID '{META_DATA_ID}' "
        f"associated with the recording ID '{RECORDING_ID}'. "
        f"The following markers were added:\n{MARKERS}"
    )
```

### **7. Create Markers and Meta data for a Recording**

- This example shows you how to use a Python script to post both new metadata and markers for a specific recording. The script will create a new metadata entry along with markers, and this metadata will be associated with a returned metadata ID. Before running this script, make sure you have set up the recording for which you are creating metadata and markers.

```python
import asyncio
import numpy as np
from datetime import datetime
from idun_data_models import Metadata_in, Marker
from config import PASSWORD
from idun_guardian_client.igeb_metadata import MetadataClient

# Configuration
DEVICE_ID = "XX-XX-XX-XX-XX-XX"  # Replace with your device ID, e.g., "XX-XX-XX-XX-XX-XX"
RECORDING_ID = "xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx"  # Replace with your recording ID
DISPLAY_NAME = "last_test"  # Optional name for the metadata
EXPERIMENT_NAME = "nap"  # Experiment name from Metadata_in enum class

# Generate Markers
MARKERS = [
    Marker(timestamp=datetime.now(), marker={"last_sleep_event": np.random.randint(10)})
    for _ in range(100)
]

# Initialize MetadataClient
client = MetadataClient(DEVICE_ID, RECORDING_ID, PASSWORD)

# Create Metadata and Markers
metadata_markers = asyncio.run(
    client.create_metadata(
        Metadata_in(
            displayName=DISPLAY_NAME,
            experiment_name=EXPERIMENT_NAME,
            markers=MARKERS,
        ),
    )
)

# Output Result
print(
    f"Succesfully created the metadata:\n{metadata_markers} with metadata ID: {metadata_markers.id}"
)
```

### **8. List meta data for a recording and metadata ID**

- This example demonstrates how to retrieve metadata associated with a specific recording. It fetches the metadata based on the metadata ID and the recording ID. Before running this script, ensure you have already posted metadata for the recording.

```python
import asyncio
import os
from config import PASSWORD
from idun_guardian_client.igeb_metadata import MetadataClient

# Configuration
META_DATA_ID = "19"  # Replace with the metadata ID associated with your recording
DEVICE_ID = "XX-XX-XX-XX-XX-XX"  # Replace with your device ID, e.g., "XX-XX-XX-XX-XX-XX"
RECORDING_ID = "xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx"  # Replace with your recording ID

# Initialize MetadataClient
client = MetadataClient(DEVICE_ID, RECORDING_ID, PASSWORD)

# Fetch Metadata
markers_list = asyncio.run(client.get_metadata(META_DATA_ID))

# Display Results
print(f"Listing the metadata associated with the recording ID {RECORDING_ID}")
for en, metadata in enumerate(markers_list):
    print(f"{metadata}\n")
```

### **9. List all markers for a recording and metadata ID**

- This example demonstrates how to add new markers to an existing metadata ID. The new markers will be associated with a given recording and metadata ID. To execute this script, make sure you have already created metadata using the create_metadata.py example.

```python
import asyncio
import numpy as np
from datetime import datetime
from idun_data_models.rest_metadata import Marker
from config import PASSWORD
from idun_guardian_client.igeb_metadata import MetadataClient

# Configuration
META_DATA_ID = "19"  # Replace with your metadata ID associated with the recording
DEVICE_ID = "XX-XX-XX-XX-XX-XX"  # Replace with your device ID, e.g., "XX-XX-XX-XX-XX-XX"
RECORDING_ID = "xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx"  # Replace with your recording ID

# Create markers
MARKERS = [
    Marker(timestamp=datetime.now(), marker={"sleepy": np.random.randint(10)})
    for _ in range(100)
]

# Initialize MetadataClient
client = MetadataClient(DEVICE_ID, RECORDING_ID, PASSWORD)

# Add Markers to Metadata
response = asyncio.run(client.create_markers(META_DATA_ID, MARKERS))

# Display Results
if response:
    print(f"Successfully added markers to metadata ID '{META_DATA_ID}' "
          f"associated with recording ID '{RECORDING_ID}'."
          f" The following markers were added:\n{MARKERS}")
```

### **10. List all meta data for a recording**

- This example demonstrates how to list all metadata entries associated with a specific recording. You can specify the number of entries to be returned in one request (LIMIT) and, if needed, where to start fetching new metadata (CURSOR).

```python
import asyncio
from datetime import datetime
from idun_data_models import (
    Metadata_in,
    Metadata_out,
    Marker,
    MAX_MARKER_COUNT,
)
from config import PASSWORD
from idun_guardian_client.igeb_metadata import MetadataClient

# Configuration
DEVICE_ID = "XX-XX-XX-XX-XX-XX"  # Replace with your device ID
RECORDING_ID = "xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx"  # Replace with your recording ID
LIMIT = 100  # Number of metadata entries to return in one request, default is 3
CURSOR = 1  # The ID of the last entry in the previous query, if needed

# Initialize MetadataClient
client = MetadataClient(DEVICE_ID, RECORDING_ID, PASSWORD)

# List Metadata
metadata_list = asyncio.run(
    client.list_metadata(
        params={
            "limit": LIMIT,
            # "cursor": CURSOR,  # Uncomment if you want to use a cursor
        },
    )
)

# Display Results
print(f"Listing the metadata associated with recording ID '{RECORDING_ID}'")
for en, metadata in enumerate(metadata_list):
    print(f"Metadata ID: {metadata.id} : {metadata}\n")
```

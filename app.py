# ENV
from dotenv import load_dotenv
from pathlib import Path  # python3 only

# RYO
from data.energy_connection import EnergyConnection
from model.series_sample import TimeSeriesSample

# Falcon
import falcon

# Load ENVS
load_dotenv()
# load_dotenv(verbose=True)  # Verbose
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


# Establish database connection
energy_connection = EnergyConnection()


def load_data():
    """Load in the sample"""
    # Load in data
    sample_frame = energy_connection.sample_series('energy_readings')
    # TODO: Rooms/QL Extract
    sample_frame = energy_connection.sample_series('external_readings', append_frame=sample_frame)

    # To object
    sample = TimeSeriesSample(sample_frame, 'time')

    return sample


class SamplesResource(object):
    def on_get(self, req, resp):
        """Sample the series into memory?"""
        sample = load_data()

        print(sample.base.describe())
        resp.status = falcon.HTTP_200

        frame_str = str(sample.base.describe()) + "\n"
        resp.body = frame_str
        # resp.body = sample.base.describe()


app = falcon.API()

# Samples api
samples = SamplesResource()
app.add_route('/samples', samples)

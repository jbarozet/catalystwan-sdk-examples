import sys

sys.path.insert(0, "..")
from catalystwan.models.configuration.feature_profile.sdwan.system.aaa import AAAParcel

from utils.session import create_session

# Create vManage session
session = create_session()

parcels = session.api.sdwan_feature_profiles.system.get_parcels("44a9f6dd-2cfc-4f87-acb7-b044368d745f", AAAParcel)

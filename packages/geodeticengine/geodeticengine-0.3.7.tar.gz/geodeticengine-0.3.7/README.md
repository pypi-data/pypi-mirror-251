# Geodetic Engine

A Python library using the Equinor Geodetic Engine API and pyproj to transform coordinates between different Coordinate Reference Systems (CRS).

## Installation

1. You need access to [Equinor Geodetic Engine API](https://api.equinor.com/api-details#api=ege-GeodeticEngine-v1), given through [AccessIT](https://accessit.equinor.com/Search/Search?term=geodetic+engine)

2. A personal subscription key is required to authenticate through APIM. Sign in to [api.equinor.com](https://api.equinor.com) and subscribe to [Enterprise](https://api.equinor.com/product#product=corporate)

3. As usual it´s installed running pip install:
```
pip install -i https://test.pypi.org/simple/ geodeticengine

```

## Authentication
There are two ways to authenticate:
- User access - MSAL Device code flow
- Application access - MSAL Client credential flow



### User-based authentication using MSAL Device code flow
When user authentication is necessary, the app generates a code and prompts the user to visit a specific URL. At the webpage, the user is asked to enter the code provided by the app. From there, the webpage will guide the user through the standard authentication and login process.

To use the package with user-based access, you will need to add the following environment variables to your system:
```
EGE_CLIENT_ENVS=prod;test
EGE_TENANT_ID=3aa4a235-b6e2-48d5-9195-7fcf05b459b0
EGE_RESOURCE_IDS=c25018ed-b371-4b37-ba4e-4d902aee2b6c;84c8d2ec-6294-47aa-8fd4-f69c870faa3a
EGE_SUBS_KEYS=<your-subscription-key-for-geodeticengine-prod;your-subscription-key-for-geodeticengine-test>
```
**EGE_CLIENT_ENVS** sets the order of environment variables. If you only have access to "prod", simply add "prod" to this variable.<br>
**EGE_TENANT_ID** is the tenant ID (Equinor).<br>
**EGE_SUBS_KEYS** is your APIM subscription keys for each environment (prod and test). This will allow the package to access the resources you have permission to use.<br>
**EGE_RESOURCE_IDS** is the resource ID of the geodetic engine for the specified environments.<br>




### Application access - MSAL Client credential flow

To use the package with application-based access, you will need to add the following environment variables to your system:
- EGE_CLIENT_IDS
- EGE_CLIENT_SECRETS

Add the following environment variables to your system:
```
EGE_TENANT_ID=3aa4a235-b6e2-48d5-9195-7fcf05b459b0
EGE_CLIENT_ENVS=prod;test
EGE_CLIENT_IDS=<your-app-id-prod;your-app-id-test>
EGE_RESOURCE_IDS=c25018ed-b371-4b37-ba4e-4d902aee2b6c;84c8d2ec-6294-47aa-8fd4-f69c870faa3a
EGE_SUBS_KEYS=<your-subscription-key-for-geodeticengine-prod;your-subscription-key-for-geodeticengine-test>
EGE_CLIENT_SECRETS=<your-app-secret-prod;your-app-secret-test>
```

When **EGE_CLIENT_SECRETS** is added, the authorization class will automatically use Application Access to authenticate.


## Access test environment
To use the package to access Geodetic Engine Test environment, you need to set the EGE_API_ENV as an environment variable.
If this environment variable is not set, the package will use the production environment.
```
EGE_API_ENV=test
```

## Token cache
The token for each environment is cached and stored in the user's home directory, eliminating the need to authenticate before every session. Although an access token expires after one hour, the presence of a cached Refresh Token allows a new Access Token to be obtained without requiring re-authentication. The Refresh Token lasts for 90 days, then you have to log in again.

## Code example

```
from geodeticengine import CoordTrans

point_in_4230 = [[10,60]]
point_in_4326 = [[9.99860677505385, 59.999554562447024]]
crs_from = "EPSG:4230"
crs_to = "EPSG:4326"
trans = "EPSG:1612"
ct = CoordTrans(crs_from=crs_from, crs_to=crs_to, trans=trans, points=point_in_4230)
print(ct.transform_pointlist_forward())

# Get pipleline
ct = CoordTrans(crs_from=crs_from, crs_to=crs_to, trans=trans)
print(ct.get_pipeline_forward())

# Inverse transformation
ct = CoordTrans(crs_from=crs_from, crs_to=crs_to, trans=trans, points=point_in_4326)
print(ct.transform_pointlist_inverse())

# Transform coordinates using pipeline
ct = CoordTrans(crs_from=crs_from, crs_to=crs_to, trans=trans)

pipeline_forward = ct.get_pipeline_forward()
print(ct.transform_from_pipeline(point_in_4230, pipeline_forward))

pipeline_inverse = ct.get_pipeline_inverse()
print(ct.transform_from_pipeline(point_in_4326, pipeline_inverse))
```
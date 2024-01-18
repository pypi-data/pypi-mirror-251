# Snapser CLI Tool

## Dependencies

The Snapser CLI tool depends on Python 3.X and Pip. MacOS comes pre installed with Python. But
please make sure you are running Python 3.X. On Windows, you can download Python 3.X from the
Windows store. Some of the commands also need docker.

## Installation

Installing PIP on MacOS

```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

Installing PIP on Windows

```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

Once you have Python and Pip installed

```
pip install --user snapctl
```

If you also have Python 2.X on your machine, you may have to run the following command instead

```
pip3 install --user snapctl
```

<Note>
  After you install snapctl you may have to add the python bin folder to your
  path. For example, on MacOSX this is usually **~/Library/Python/3.9/bin**. On
  Windows this is usually
  **C:\Users\username\AppData\Roaming\Python\Python39\Scripts**.
</Note>

## Upgrade

Upgrade your snapctl version

```
pip install --user snapctl --upgrade
```

## Setup

### Get your Snapser Access Key

Log in to your Snapser account. Click on your user icon on the top right and select, User Account.
In the left navigation click on **Developer** which will bring up your Personal API Key widget.
If you have not generated an API Key yet click on the **Generate** button to generate a new key.
You can generate up to 3 API Keys per user account.

<Note>
  Please make sure you save your API key in a safe place. You will not be able
  to see it again.
</Note>

### Setup a local config

Create a file named `~/.snapser/config`. Open it using the editor of your choice and replace with your
personal Snapser Access key. Save the file.

```
[default]
snapser_access_key = <key>
```

Or you can run the following command

on MacOSX

```
# $your_api_key = Your Snapser developer key
echo -e "[default]\nSNAPSER_API_KEY=$your_api_key" > ~/.snapser/config
```

on Windows Powershell

```
# $your_api_key = Your Snapser developer key
echo "[default]
SNAPSER_API_KEY=$your_api_key" | Out-File -encoding utf8 ~\.snapser\config
```

## Verify Snapctl installation

```
snapctl --version
```

You should see the latest snapctl version in the output

## Advanced Setup

Snapser by default supports access to multiple accounts. You can create multiple profiles in your Snapser config
**~/.snapser/config**.

```
[profile personal]
snapser_access_key = <key>

[profile professional]
snapser_access_key = <key>

```

You can then set an environment variable telling Snapser which profile you want to use.

```
# Mac
export SNAPSER_PROFILE="my_profile_name";

```

```
# Windows
setx SNAPSER_PROFILE="my_profile_name";

```

Or you can pass **--profile my_profile_name** with every command to tell Snapser to use a particular profile.

## Commands

Run the following to see the list of commands Snapser supports

```
snapctl --help
```

### BYO Snap - Bring your own Snap

#### 1. byosnap help

See all the supported commands

```
# Help for the byosnap command
snapctl byosnap --help
```

#### 2. byosnap create

Ability to create a custom snap.

```
# Help for the byosnap command
snapctl byosnap create --help

# Create a new snap
# $byosnap_sid = Snap ID for your snap. Start start with `byosnap-`
# $name = User friendly name for your BYOSnap
# $desc = User friendly description
# $platform = One of linux/arm64, linux/amd64
# $language = One of go, python, ruby, c#, c++, rust, java, node

# Example:
# snapctl byosnap create byosnap-jinks-flask --name "Jinks Flask Microservice" --desc "Custom Microservice" --platform "linux/arm64" --language "go"
snapctl byosnap create $byosnap_sid --name "$name" --desc "$desc" --platform "$platform" --language "$language"
```

#### 3. byosnap publish-image

Ability to publish a custom snap code image.

```
# Help for the byosnap command
snapctl byosnap publish-image --help

# Publish a new image
# $byosnap_sid = Snap ID for your snap
# $image_tag = An image tag for your snap
# $code_root_path = Local code path where your Dockerfile is present
# Example:
# snapctl byosnap publish-image byosnap-jinks-flask --tag my-first-image --path /Users/DevName/Development/SnapserEngine/jinks_flask
snapctl byosnap publish-image $byosnap_sid --tag $image_tag --path $code_root_path
```

#### 4. byosnap publish-version

Ability to publish a new version for your Snap.

```
# Help for the byosnap command
snapctl byosnap publish-version --help

# Publish a new image
# $byosnap_sid = Snap ID for your snap
# $image_tag = An image tag for your snap
# $prefix = Prefix for your snap Eg: /v1
# $version = Semantic version for your snap Eg: v0.0.1
# $ingress_port = Ingress port for your snap Eg: 5003
# Example:
# snapctl byosnap publish-image byosnap-jinks-flask --tag my-first-image --prefix /v1 --version v0.0.1 --http-port 5003
snapctl byosnap publish-version $byosnap_sid --tag $image_tag --prefix $prefix --version $version --http-port $ingress_port
```

#### 5. byosnap upload-docs

Ability to upload swagger.json and README.md for you Snap

```
# Help for the byogs command
snapctl byosnap upload-docs --help

# Publish a new image
# $byogs_sid = Game server ID for your snap
# $image_tag = An image tag for your snap
# $code_root_path = Local code path where your swagger.json and README.md files are present
# Example:
# snapctl byosnap upload-docs byosnap-jinks-flask --tag my-first-image --path /Users/DevName/Development/SnapserEngine/jinks_flask
snapctl byosnap upload-docs $byogs_sid --tag $image_tag --path $code_root_path
```

### BYO Game Server - Bring your own Game Server

#### 1. byogs help

See all the supported commands

```
# Help for the byogs command
snapctl byogs --help
```

#### 2. byogs create

Ability to create a custom game server.

```
# Help for the byosnap command
snapctl byogs create --help

# Create a new snap
# $byogs_sid = Game server ID for your snap. Should start with `byogs-`
# $name = User friendly name for your BYOGs
# $desc = User friendly description
# $platform = Currently only supported platform is linux/amd64
# $language = One of go, python, ruby, c#, c++, rust, java, node

# Example:
# snapctl byogs create byosnap-jinks-gs --name "Jinks Flask Microservice" --desc "Custom Microservice" --platform "linux/arm64" --language "go"
snapctl byogs create $byogs_sid --name "$name" --desc "$desc" --platform "$platform" --language "$language"
```

#### 3. byogs publish-image

Ability to publish your custom game server image.

```
# Help for the byogs command
snapctl byogs publish-image --help

# Publish a new image
# $byogs_sid = Game server ID for your snap
# $image_tag = An image tag for your snap
# $code_root_path = Local code path where your Dockerfile is present
# Example:
# snapctl byogs publish-image byosnap-jinks-gs --tag my-first-image --path /Users/DevName/Development/SnapserEngine/jinks_flask
snapctl byogs publish-image $byogs_sid --tag $image_tag --path $code_root_path
```

#### 4. byogs publish-version

Ability to publish a new version for your Game server.

```
# Help for the byogs command
snapctl byogs publish-version --help

# Publish a new image
# $byogs_sid = Snap ID for your snap
# $image_tag = Any image tag for your snap
# $prefix = Prefix for your snap Eg: /v1
# $version = Semantic version for your snap Eg: v0.0.1
# $ingress_port = Ingress port for your snap Eg: 5003
# Example:
# snapctl byogs publish-image byosnap-jinks-gs --tag my-first-image --prefix /v1 --version v0.0.1 --http-port 5003
snapctl byogs publish-version $byogs_sid --tag $image_tag --prefix $prefix --version $version --http-port $ingress_port
```

### Snapend

#### 1. snapend help

See all the supported commands

```
# Help for the byogs command
snapctl snapend --help
```

#### 2. Snapend Downloads

Download SDKs and Protos for your Snapend

```
# Help for the byogs command
snapctl snapend download --help

# Download your Snapend SDK and Protos
# $snapend_id = Cluster Id
# $category = client-sdk, server-sdk, protos, admin-settings
# $sdk_type = One of the supported SDK names:
# client-sdk(unity, unreal, roblox, godot, cocos, ios-objc, ios-swift, android-java, android-kotlin, web-ts, web-js),
# server-sdk(csharp, cpp, lua, ts, go, python, kotlin, java, c, node, js, perl, php, closure, ruby, rust),
# protos(go)
# Example:
# snapctl snapend download gx5x6bc0 --category client-sdk --type unity
snapctl snapend download $snapend_id --category $category --type $sdk_type
```

#### 3. Update Snapend BYOSnap or BYOGs versions

Update your BYOSnap or BYOGs versions for the Snapend

```
# Help for the byogs command
snapctl snapend update --help

# Update your Snapend with new BYOSnaps and BYOGs
# $snapend_id = Cluster Id
# $byosnaps = Comma separated list of BYOSnap ids and version.
# $byogs = Comma separated list of BYOGs fleet name, id and version.
# --blocking = (Optional) This makes sure the CLI waits till your Snapend is live.
# Note at least one of the two needs to be present
# Example:
# snapctl snapend update gx5x6bc0 --byosnaps byosnap-service-1:v1.0.0,byosnap-service--2:v1.0.0 --byogs byogs-fleet-one:gs-1:v0.0.1,my-fleet-two:gs-2:v0.0.4
# snapctl snapend update gx5x6bc0 --byosnaps byosnap-service-1:v1.0.0,byosnap-service--2:v1.0.0 --byogs byogs-fleet-one:gs-1:v0.0.1,my-fleet-two:gs-2:v0.0.4 --blocking
snapctl snapend update $snapend_id --byosnaps $byosnaps --byogs $byogs --blocking
```

#### 4. Get the Snapend state

Get the Snapend state

```
# Help for the byogs command
snapctl snapend state --help

# Get the Snapend state
# $snapend_id = Cluster Id
# Example:
# snapctl snapend state gx5x6bc0
snapctl snapend state $snapend_id
```

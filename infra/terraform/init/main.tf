# define provider required to provision
# providers can be found in teraform registry
terraform {
  # backend "remote" {
  #   organization = "mansourmahboubi"
  #   workspaces {
  #     name = "first-ws"
  #   }

  # }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

# sepcify provider
provider "aws" {
  # is not required in tfm cloud
  profile = "default"

  region = "eu-west-3"
}

# physical or virtual component
# ec2 or logical like herouku app

# resourse type and resourse name the name maps to provider
# resourse name
# type and name will create a uniuque ID
resource "aws_instance" "app_server" {
  # ami is somekind of template
  #   https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/finding-an-ami.html#finding-quick-start-amis
  ami           = "ami-084419b01954a6223"
  instance_type = "t2.micro"

  tags = {
    Name = var.instance_name
  }
}

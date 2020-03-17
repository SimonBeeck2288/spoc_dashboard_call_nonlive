#!/bin/bash



ACCOUNT_ID="925522540492"

CURRENT_ACCOUNT_ID=$(aws sts get-caller-identity --query 'Account' --output text)

if [[ "${ACCOUNT_ID}" != "${CURRENT_ACCOUNT_ID}" ]]; then
	echo "Please deploy only in spoc nonlive"
	echo "Execute . awsume spoc-nonlive-admin"
	exit 1
fi

rm -rf ~/callTest/src 
cp -rf /media/sf_Ubuntushared/callTest/src/ ~/callTest/src 
chmod 777 ~/callTest/src/callTest.py 
rm ~/callTest/template.yaml 
cp /media/sf_Ubuntushared/callTest/template.yaml ~/callTest/template.yaml 
sam=$(which sam)
sam build
sam deploy --guided
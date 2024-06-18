ecr="non-prod-ttn-sws-log-image"
imgTag="fluentbit-latest"
dockerTag="non-prod-ttn-sws-fluentbit"
repo_num="204184355380"
region="ap-south-1"

aws ecr get-login-password --region $region | docker login --username AWS --password-stdin $repo_num.dkr.ecr.$region.amazonaws.com

docker buildx build --platform linux/amd64,linux/arm64 --no-cache -f Dockerfile -t $dockerTag  . &&
    docker tag $dockerTag:latest $repo_num.dkr.ecr.$region.amazonaws.com/$ecr:$imgTag &&
    docker push $repo_num.dkr.ecr.$region.amazonaws.com/$ecr:$imgTag

echo "Image Pushed"
echo "$repo_num.dkr.ecr.$region.amazonaws.com/$ecr:$imgTag"

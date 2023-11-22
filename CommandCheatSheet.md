
## Progress checking

### Once the job has started but the shell has disconnected

- ssh over to the EC2 (`sh aws-scripts/connect-to-image-builder.sh`)
- `docker ps` # get the running process based on command
- docker logs `Container ID` or `Container Name`

## Git

### Clear out all the training branches
git branch | grep 'training' | xargs git branch -d

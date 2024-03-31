# application-example
業務で使う前に色々と検証するためのアレ (アプリの方)

# Requirements
- Docker
- GNU Make
- diernv

# Prepare
 - $mv .envrc.template .envrc
 - $vi .envrc # replace *AWS_PROFILE* *AWS_ACCOUNT*
 - $direnv allow

# Initialize
- $ make up
- (wait for while until mysql initialization is done)
- $ make db upgrade

# Run app
- $ make up-watch

# Listening ports
Customer web
- http://localhost:80

Administrator web
- https://localhost:8080

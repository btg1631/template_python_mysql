FROM python:3.11

# 작업 디렉토리 설정
WORKDIR /app

ARG GIT_BRANCH_NAME
ARG APP_DIR_NAME
ARG GITHUB_URI

# Clone the Git repository. Here we dynamically specify the repository name using the variable defined earlier.
RUN git clone -b ${GIT_BRANCH_NAME} ${GITHUB_URI} ${APP_DIR_NAME}

# Changes the working directory to /app/${REPO_NAME}. This uses the variable to dynamically set the directory path.
WORKDIR /app/${APP_DIR_NAME}

RUN pip install --no-cache-dir -r ./requirements.txt

RUN rm -rf .git
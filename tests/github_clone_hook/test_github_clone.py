import pytest
import git


def clone_repo(repo_url, clone_dir):
    try:
        git.Repo.clone_from(repo_url, clone_dir)
        print(f"Repository cloned to {clone_dir}")
    except Exception as e:
        print(f"Error: {e}")


@pytest.mark.order(1)
def test_can_clone_github_my_repo():
    # given : 유효한 repo 경로
    repo_url = "https://github.com/brickstudy/ETL.git"
    clone_dir = './ETL'

    # when : clone 요청
    clone_repo(repo_url, clone_dir)

    # then : repo clone
    # print(result.stdout)

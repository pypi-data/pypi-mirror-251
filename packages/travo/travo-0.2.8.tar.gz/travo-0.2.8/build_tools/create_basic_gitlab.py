import os
import gitlab
import requests
from urllib.parse import urljoin

if "GITLAB_HOST" in os.environ and "GITLAB_80_TCP_PORT" in os.environ:
    gitlab_url = f"http://{os.environ['GITLAB_HOST']}:{os.environ['GITLAB_80_TCP_PORT']}"
else:
    gitlab_url = "http://gitlab"

# Password authentification is no longer supported by python-gitlab
# https://python-gitlab.readthedocs.io/en/stable/api-usage.html#note-on-password-authentication
data = {'grant_type': 'password', 'username': 'root', 'password': 'dr0w554p!&ew=]gdS'}
resp = requests.post(urljoin(gitlab_url, 'oauth/token'), data=data)
resp_data = resp.json()
gitlab_oauth_token = resp_data['access_token']

# login
gl = gitlab.Gitlab(gitlab_url, oauth_token=gitlab_oauth_token)

# create users
user_data = {'username': 'travo-test-etu', 'email': 'travo@gmail.com', 'name': 'Étudiant de test pour travo', 'password': 'aqwzsx(t1', 'can_create_group': 'True'}
gl.users.create(user_data)
other_user_data = {'username': 'blondin_al', 'email': 'blondin_al@blondin_al.fr', 'name': 'Utilisateur de test pour travo', 'password': 'aqwzsx(t2'}
gl.users.create(other_user_data)

# create user projects and groups
user = gl.users.list(username='travo-test-etu')[0]
user.projects.create({'name': 'nom-valide', 'visibility': 'private'})
user.projects.create({'name': 'Fork-de-travo-test-etu-du-projet-Exemple-projet-CICD', 'visibility': 'private'})
group = gl.groups.create({'name': 'group1', 'path': 'group1'})
group.members.create({'user_id': user.id, 'access_level': gitlab.const.AccessLevel.DEVELOPER})
subgroup = gl.groups.create({'name': 'subgroup', 'path': 'subgroup', 'parent_id': group.id})
grouppublic = gl.groups.create({'name': 'Groupe public test', 'path': 'groupe-public-test', 'visibility': 'public'})
project = gl.projects.create({'name': 'Projet public', 'visibility': 'public', 'namespace_id': grouppublic.id})

# create commits
# See https://docs.gitlab.com/ce/api/commits.html#create-a-commit-with-multiple-files-and-actions
# for actions detail
data = {
    'branch': 'master',
    'commit_message': 'blah blah blah',
    'author_name': user.name,
    'author_email': user.email,
    'actions': [
        {
            'action': 'create',
            'file_path': 'README.md',
            'content': 'This is a README.',
        },
    ]
}

commit = project.commits.create(data)

# general settings for project export and import 
settings = gl.settings.get()
settings.max_import_size = 50
settings.import_sources = ['git', 'gitlab_project']
settings.save()

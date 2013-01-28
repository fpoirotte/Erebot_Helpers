# -*- coding: utf-8 -*-
import sys
import urllib2
import argparse
import json
import secrets

class GHAPI(urllib2.Request):
    def __init__(self, url, data=None, headers=None, origin_req_host=None, unverifiable=False):
        if headers is None:
            headers = {}
        headers['Authorization'] = 'token %s' % secrets.GITHUB_API_TOKEN
        if not url.startswith('/'):
            url = '/' + url
        url = 'https://api.github.com%s' % url
        urllib2.Request.__init__(self, url, data, headers, origin_req_host, unverifiable)

def gh_api(url, data=None, raw=False):
    headers = None
    if data != None:
        data = json.dumps(data)
    res = urllib2.urlopen(GHAPI(url, data))
    if raw:
        return res
    return json.load(res)

def main():
    print "Retrieving list of repositories...",
    sys.stdout.flush()
    resp = gh_api('/orgs/Erebot/repos?per_page=100')
    repos = [r['full_name'] for r in resp]
    resp = gh_api('/user/repos?per_page=100')
    repos += [r['full_name'] for r in resp]
    repos.sort()
    print "OK (%d found)" % len(repos)
    sys.stdout.flush()

    for repo in repos:
        print ("Updating hooks for %s..." % repo),
        sys.stdout.flush()
        hooks = gh_api('/repos/%s/hooks?per_page=100' % repo)
        for hook in hooks:
            if not (
                hook['name'] == 'web' and
                hook['active'] == True and
                'erebot.net' in hook['config']['url']):
                continue
            resp = gh_api(
                '/repos/%s/hooks/%s' % (repo, hook['id']),
                {
                    'name': 'web',
                    'config': {
                        'url': secrets.GITHUB_URL,
                        'insecure_ssl': True,
                        'content_type': 'json',
                        'secret': secrets.GITHUB_KEY,
                    },
                    'events': ['push'],
                    'active': True,
                }
            )
        print "OK"
        sys.stdout.flush()
    headers = gh_api('/rate_limit', raw=True).info()
    print "Done updating every last hook! (credits left: %s/%s)" % (
        headers.getheader('X-RateLimit-Remaining'),
        headers.getheader('X-RateLimit-Limit'),
    )

if __name__ == '__main__':
    main()

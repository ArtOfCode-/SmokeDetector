# -*- coding: utf-8 -*-
import regex


def likely_vlq(s, site):
    if len(s) <= 200:
        reg = regex.compile(ur"(?i)((present|past)( perfect)?|modals?|auxiliar(y|ies))")
        if reg.findall(s):
            match = "".join(["".join(match) for match in matches])
            return True, "Short post mentioning {}".format(match)

    return False, ""

def confusion(s, site):
    if len(s) <= 200:
        reg = regex.compile(ur"(?i)(confused|don\'t understand|hav(ing)? problems?)")
        if reg.search(s):
            return True, "Confusion in a short post"

    return False, ""


class FindSpam:
    with open("bad_keywords.txt", "r") as f:
        bad_keywords = [line.decode('utf8').rstrip() for line in f if len(line.decode('utf8').rstrip()) > 0]

    bad_keywords_nwb = []

    with open("blacklisted_websites.txt", "r") as f:
        blacklisted_websites = [line.rstrip() for line in f if len(line.rstrip()) > 0]

    with open("blacklisted_usernames.txt", "Ur") as f:
        blacklisted_usernames = [line.rstrip() for line in f if len(line.rstrip()) > 0]

    # Patterns: the top three lines are the most straightforward, matching any site with this string in domain name
    pattern_websites = []

    city_list = []
    rules = [
        {'regex': ur"(?is)\b({})\b|{}".format("|".join(bad_keywords), "|".join(bad_keywords_nwb)), 'all': False,
         'sites': ['english.stackexchange.com'], 'reason': "bad keyword in {}", 'title': True, 'body': True, 'username': True, 'stripcodeblocks': False,
         'body_summary': True, 'max_rep': 4, 'max_score': 1},
        {'regex': u"(?i)({})".format("|".join(blacklisted_websites)), 'all': False,
         'sites': ['english.stackexchange.com'], 'reason': "blacklisted website in {}", 'title': True, 'body': True, 'username': False, 'stripcodeblocks': False,
         'body_summary': True, 'max_rep': 50, 'max_score': 5},
        {'regex': ur"(?i)({}|({})[\w-]*?\.(co|net|org|in\W|info|blogspot|wordpress))(?![^>]*<)".format("|".join(pattern_websites), "|".join(bad_keywords_nwb)), 'all': False,
         'sites': ['english.stackexchange.com'], 'reason': "pattern-matching website in {}", 'title': True, 'body': True, 'username': False, 'stripcodeblocks': True,
         'body_summary': True, 'max_rep': 1, 'max_score': 1},
        {'regex': ur"(?i)({})".format("|".join(blacklisted_usernames)), 'all': False,
         'sites': ['english.stackexchange.com'], 'reason': "blacklisted username", 'title': False, 'body': False, 'username': True, 'stripcodeblocks': False,
         'body_summary': False, 'max_rep': 1, 'max_score': 0},
        {'method': likely_vlq, 'all': False,
         'sites': ['english.stackexchange.com'], 'reason': 'possible low-quality post', 'title': False, 'body': True, 'username': False, 'stripcodeblocks': False,
         'body_summary': False, 'max_rep': 1, 'max_score': 0},
        {'regex': ur"(?i)can.{0,15}(explain|help) (to )?me", 'all': False,
         'sites': ['english.stackexchange.com'], 'reason': 'request for explanation', 'title': False, 'body': True, 'username': False, 'stripcodeblocks': False,
         'body_summary': False, 'max_rep': 1, 'max_score': 0},
        {'method': confusion, 'all': False,
         'sites': ['english.stackexchange.com'], 'reason': 'possible low-quality post', 'title': False, 'body': True, 'username': False, 'stripcodeblocks': False,
         'body_summary': False, 'max_rep': 1, 'max_score': 0}
    ]

    @staticmethod
    def test_post(title, body, user_name, site, is_answer, body_is_summary, user_rep, post_score):
        result = []
        why = {'title': [], 'body': [], 'username': []}
        for rule in FindSpam.rules:
            body_to_check = body
            is_regex_check = 'regex' in rule
            try:
                check_if_answer = rule['answers']
            except KeyError:
                check_if_answer = True
            try:
                check_if_question = rule['questions']
            except KeyError:
                check_if_question = True
            body_to_check = regex.sub("[\xad\u200b\u200c]", "", body_to_check)
            if rule['stripcodeblocks']:    # use a placeholder to avoid triggering "few unique characters" when most of post is code
                body_to_check = regex.sub("(?s)<pre>.*?</pre>", u"<pre><code>placeholder for omitted code/код block</pre></code>", body_to_check)
                body_to_check = regex.sub("(?s)<code>.*?</code>", u"<pre><code>placeholder for omitted code/код block</pre></code>", body_to_check)
            if rule['reason'] == 'Phone number detected in {}':
                body_to_check = regex.sub("<img[^>]+>", "", body_to_check)
                body_to_check = regex.sub("<a[^>]+>", "", body_to_check)
            if rule['all'] != (site in rule['sites']) and user_rep <= rule['max_rep'] and post_score <= rule['max_score']:
                matched_body = None
                compiled_regex = None
                if is_regex_check:
                    compiled_regex = regex.compile(rule['regex'], regex.UNICODE, city=FindSpam.city_list)  # using a named list \L in some regexes
                    matched_title = compiled_regex.findall(title)
                    matched_username = compiled_regex.findall(user_name)
                    if (not body_is_summary or rule['body_summary']) and (not is_answer or check_if_answer) and (is_answer or check_if_question):
                        matched_body = compiled_regex.findall(body_to_check)
                else:
                    assert 'method' in rule
                    matched_title, why_title = rule['method'](title, site)
                    if matched_title and rule['title']:
                        why["title"].append(u"Title - {}".format(why_title))
                    matched_username, why_username = rule['method'](user_name, site)
                    if matched_username and rule['username']:
                        why["username"].append(u"Username - {}".format(why_username))
                    if (not body_is_summary or rule['body_summary']) and (not is_answer or check_if_answer) and (is_answer or check_if_question):
                        matched_body, why_body = rule['method'](body_to_check, site)
                        if matched_body and rule['body']:
                            why["body"].append(u"Post - {}".format(why_body))
                if matched_title and rule['title']:
                    why["title"].append(FindSpam.generate_why(compiled_regex, title, u"Title", is_regex_check))
                    result.append(rule['reason'].replace("{}", "title"))
                if matched_username and rule['username']:
                    why["username"].append(FindSpam.generate_why(compiled_regex, user_name, u"Username", is_regex_check))
                    result.append(rule['reason'].replace("{}", "username"))
                if matched_body and rule['body']:
                    why["body"].append(FindSpam.generate_why(compiled_regex, body_to_check, u"Body", is_regex_check))
                    type_of_post = "answer" if is_answer else "body"
                    result.append(rule['reason'].replace("{}", type_of_post))
        result = list(set(result))
        result.sort()
        why = "\n".join(filter(None, why["title"]) + filter(None, why["body"]) + filter(None, why["username"])).strip()
        return result, why

    @staticmethod
    def generate_why(compiled_regex, matched_text, type_of_text, is_regex_check):
        if is_regex_check:
            matches = compiled_regex.finditer(matched_text)
            why_for_matches = []
            for match in matches:
                span = match.span()
                group = match.group()
                why_for_matches.append(u"Position {}-{}: {}".format(span[0] + 1, span[1] + 1, group))
            return type_of_text + u" - " + ", ".join(why_for_matches)
        return ""

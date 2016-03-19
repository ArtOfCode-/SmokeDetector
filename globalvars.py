# -*- coding: utf-8 -*-

import os
from datetime import datetime
from ChatExchange.chatexchange.client import Client
import HTMLParser
import md5
import ConfigParser


class GlobalVars:
    false_positives = []
    whitelisted_users = []
    blacklisted_users = []
    ignored_posts = []
    auto_ignored_posts = []
    startup_utc = datetime.utcnow().strftime("%H:%M:%S")
    latest_questions = []
    blockedTime = 0
    api_backoff_time = 0
    charcoal_room_id = "11540"
    meta_tavern_room_id = "89"
    socvr_room_id = "41570"
    site_filename = {"electronics.stackexchange.com": "ElectronicsGood.txt",
                     "gaming.stackexchange.com": "GamingGood.txt", "german.stackexchange.com": "GermanGood.txt",
                     "italian.stackexchange.com": "ItalianGood.txt", "math.stackexchange.com": "MathematicsGood.txt",
                     "spanish.stackexchange.com": "SpanishGood.txt", "stats.stackexchange.com": "StatsGood.txt"}

    experimental_reasons = []  # Don't widely report these
    non_tavern_reasons = ["All-caps title",   # Don't report in the Tavern
                          "All-caps body",
                          "All-caps answer",
                          "All-caps body, all-caps title",
                          "Repeating characters in body",
                          "Repeating characters in title",
                          "Repeating characters in answer",
                          "Few unique characters in body",
                          "Few unique characters in answer",
                          "Title has only one unique char",
                          "Phone number detected in title",
                          "Offensive body detected",
                          "Email in answer",
                          "Email in title",
                          "Link at end of answer"]
    non_tavern_sites = ["stackoverflow.com"]

    parser = HTMLParser.HTMLParser()
    wrap = Client("stackexchange.com")
    wrapm = Client("meta.stackexchange.com")
    wrapso = Client("stackoverflow.com")
    privileged_users = {}
    smokeDetector_user_id = {charcoal_room_id: "120914", meta_tavern_room_id: "266345",
                             socvr_room_id: "3735529"}

    censored_committer_names = {"3f4ed0f38df010ce300dba362fa63a62": "Undo1"}

    commit = os.popen('git log --pretty=format:"%h" -n 1').read()
    commit_author = os.popen('git log --pretty=format:"%cn" -n 1').read()

    if md5.new(commit_author).hexdigest() in censored_committer_names:
        commit_author = censored_committer_names[md5.new(commit_author).hexdigest()]

    commit_with_author = os.popen('git log --pretty=format:"%h (' + commit_author + ': *%s*)" -n 1').read()
    on_master = os.popen("git rev-parse --abbrev-ref HEAD").read().strip() == "master"
    charcoal_hq = None
    tavern_on_the_meta = None
    socvr = None
    s = ""
    s_reverted = ""
    specialrooms = []
    apiquota = -1
    bodyfetcher = None
    se_sites = []
    users_chatting = {meta_tavern_room_id: [], socvr_room_id: [], charcoal_room_id: []}
    why_data = []
    why_data_allspam = []
    notifications = []
    listen_to_these_if_edited = []
    multiple_reporters = []
    api_calls_per_site = {}

    config = ConfigParser.RawConfigParser()
    config.read('config')

    latest_smokedetector_messages = {meta_tavern_room_id: [], charcoal_room_id: [],
                                     socvr_room_id: []}

    site_id_dict = {}
    post_site_id_to_question = {}
    special_room_reports = {}

    location = config.get("Config", "location")
    print location

    try:
        metasmoke_host = config.get("Config", "metasmoke_host")
        print metasmoke_host
    except ConfigParser.NoOptionError:
        metasmoke_host = None
        print "metasmoke host not found. Set it as metasmoke_host in the config file. See https://github.com/Charcoal-SE/metasmoke."

    try:
        metasmoke_key = config.get("Config", "metasmoke_key")
    except ConfigParser.NoOptionError:
        metasmoke_key = ""
        print "No metasmoke key found, which is okay if both are running on the same host"

# -*- coding: utf-8 -*-

import os
from datetime import datetime
from ChatExchange.chatexchange.client import Client
import HTMLParser
import md5
import ConfigParser
from helpers import environ_or_none
import threading


class GlobalVars:
    false_positives = []
    whitelisted_users = []
    blacklisted_users = []
    ignored_posts = []
    auto_ignored_posts = []
    startup_utc = datetime.utcnow().strftime("%H:%M:%S")
    latest_questions = []
    api_backoff_time = 0
    charcoal_room_id = "49780"
    meta_tavern_room_id = "89"
    socvr_room_id = "41570"
    blockedTime = {"all": 0, charcoal_room_id: 0, meta_tavern_room_id: 3.2e7, socvr_room_id: 3.2e7}

    experimental_reasons = []  # Don't widely report these
    non_socvr_reasons = []    # Don't report to SOCVR
    non_tavern_reasons = [    # Don't report in the Tavern
        "all-caps body",
        "all-caps answer",
        "repeating characters in body",
        "repeating characters in title",
        "repeating characters in answer",
        "few unique characters in body",
        "few unique characters in answer",
        "title has only one unique char",
        "phone number detected in title",
        "offensive body detected",
        "no whitespace in body",
        "no whitespace in answer",
    ]
    non_tavern_sites = ["stackoverflow.com"]

    parser = HTMLParser.HTMLParser()
    wrap = Client("stackexchange.com")
    wrapm = Client("meta.stackexchange.com")
    wrapso = Client("stackoverflow.com")
    privileged_users = {
        charcoal_room_id: [
            "73046",    # Undo
            "121520",   # ArtOfCode
            "164318",   # Glorfindel
            "56166",    # Jan Dvorak
            "68718",    # Wrzlprmft
            "62118"     # tripleee
        ],
        meta_tavern_room_id: [],
        socvr_room_id: []
    }

    code_privileged_users = None

    smokeDetector_user_id = {charcoal_room_id: "120914", meta_tavern_room_id: "266345",
                             socvr_room_id: "3735529"}

    censored_committer_names = {"3f4ed0f38df010ce300dba362fa63a62": "Undo1"}

    commit = os.popen('git log --pretty=format:"%h" -n 1').read()
    commit_author = os.popen('git log --pretty=format:"%an" -n 1').read()

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
    users_chatting = {meta_tavern_room_id: [], charcoal_room_id: [], socvr_room_id: []}
    why_data = []
    why_data_allspam = []
    notifications = []
    listen_to_these_if_edited = []
    multiple_reporters = []
    api_calls_per_site = {}

    api_request_lock = threading.Lock()

    config = ConfigParser.RawConfigParser()

    if os.path.isfile('config'):
        config.read('config')
    else:
        config.read('config.ci')

    latest_smokedetector_messages = {meta_tavern_room_id: [], charcoal_room_id: [], socvr_room_id: []}

    # environ_or_none defined in helpers.py
    bot_name = environ_or_none("SMOKEDETECTOR_NAME") or "SmokeDetector"
    bot_repository = environ_or_none("SMOKEDETECTOR_REPO") or "//github.com/Charcoal-SE/SmokeDetector"
    chatmessage_prefix = "[{}]({})".format(bot_name, bot_repository)

    site_id_dict = {}
    post_site_id_to_question = {}

    location = config.get("Config", "location")
    print location

    metasmoke_ws = None

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

    try:
        metasmoke_ws_host = config.get("Config", "metasmoke_ws_host")
    except ConfigParser.NoOptionError:
        metasmoke_ws_host = ""
        print "No metasmoke websocket host found, which is okay if you're anti-websocket"

    try:
        github_username = config.get("Config", "github_username")
        github_password = config.get("Config", "github_password")
    except ConfigParser.NoOptionError:
        github_username = None
        github_password = None

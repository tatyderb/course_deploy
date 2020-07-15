'''
put_step_dict = {
    "stepSource": {
        "lesson_id": 239930,                        # set lesson_id - нет в get
        "lesson": 239930,                           # set lesson_id
        "position": 1,                              # set step position in lesson, start with 1.
        "status": "ready",

        "block": {
            "name": "text",
            "text": "<p>Text of step</p>",          # set new text as html
            "video": None,
            "animation": None,
            "options": {},
            "subtitle_files": [],
            "source": {},
            "subtitles": {},
            "tests_archive": None,
            "feedback_correct": "",
            "feedback_wrong": ""
        },

        "actions": {},

        "instruction": None,
        "instruction_type": None,
        "instruction_id": None,                     # нет в get
        "has_instruction": False,                   # нет в get

        "is_solutions_unlocked": False,
        "solutions_unlocked_attempts": 3,
        "max_submissions_count": 3,
        "has_submissions_restrictions": False,

        "create_date": "2019-06-26T05:01:47Z",      # set create date

        "reason_of_failure": "",
        "error": {
            "text": "",
            "code": "",
            "params": {}
        },
        "warnings": [],
        "cost": 0,
    }
}
'''

'''
get_step_dict = {
  "meta": {
    "page": 1,
    "has_next": false,
    "has_previous": false
  },
  "step-sources": [
    {
      "id": 761415,                         # lesson_id в get dict
      "lesson": 239930,
      "position": 1,
      "status": "ready",
      "block": {
        "name": "text",
        "text": "<p>Урок 239930 шаг 1 (761415)</p>",
        "video": null,
        "animation": null,
        "options": {},
        "subtitle_files": [],
        "source": {},
        "subtitles": {},
        "tests_archive": null,
        "feedback_correct": "",
        "feedback_wrong": ""
      },
      "actions": {},
      "progress": "77-761415",      # нет в put
      "subscriptions": [            # нет в put
        "31-77-761415",
        "30-77-761415"
      ],
      "instruction": null,
      "session": null,
      "instruction_type": null,
      "viewed_by": 1,               # нет в put
      "passed_by": 1,               # нет в put
      "correct_ratio": null,        # нет в put
      "worth": 0,                   # нет в put

      "is_solutions_unlocked": false,
      "solutions_unlocked_attempts": 3,
      "max_submissions_count": 3,
      "has_submissions_restrictions": false,

      "create_date": "2019-06-26T05:01:47Z",
      "update_date": "2019-07-09T14:09:28Z",

      "variation": 1,
      "variations_count": 1,
      "discussions_count": 0,
      "discussion_proxy": "77-761415-1",
      "discussion_threads": [
        "77-761415-1"
      ],

      "reason_of_failure": "",
      "error": {
        "text": "",
        "code": "",
        "params": {}
      },
      "warnings": [],
      "cost": 0
    }
  ]
}
'''



## On the web

```

                                		GAME-SESSION         PAGE-NAME
                                            |                  |   PAGE-NUMBER
																					  v                  v   V
https://rcodi-energy-game.herokuapp.com/p/03hyj25a/training/Intro2/2/
|------|-----------------|--------------|---------|--------|
				 HEROKU-PROJ-NAME							  |          APP_PATH
                                      PAGE	       (settings.py at SESSION_CONFIGS  
                                                      ```name = "<aapp_name>"```
                                                    or to set to something different
                                                    in <app_name>/constants.py set
                                                      ```name_in_url = 'training'```
```



```
                NOTE: The HTML template
      is usually a file with same name
      as the page namein the url
      |
      PAGE-NAME |       Number in the overall  since          
    |   |-------sequence the session started
    v   V        
/training/Intro2/2/
|--------|
```


## IN THE PROJECT FILES

### MAIN SETTINGS
```
Procfile
manage.py
requirements_base.txt
requirements.txt
_rooms/test_room.txt
settings.py
db.sqlite3Procfile
manage.py
requirements_base.txt
requirements.txt
_rooms/test_room.txt
settings.py
```
### GLOBAL TEMPLATES

```
_templates/global/Page.html
_templates/global/Page.html
_templates/blocks/card-content.html
_templates/global/MTurkPreview.html
_templates/global/MTurkPreview.html
_templates/blocks/card-content.html
_templates/blocks/card-footer.html
_templates/blocks/card-footer.html
_templates/blocks/card-header.html
_templates/blocks/card-header.html
_templates/blocks/form-table.html
_templates/blocks/form-table.html
_templates/blocks/main-card.html
_templates/blocks/main-card.html
_templates/blocks/message-box.html
_templates/blocks/message-box.html
_templates/blocks/next-button.html
_templates/blocks/next-button.html
_templates/blocks/progress-steps.html
_templates/blocks/progress-steps.html
_templates/blocks/progress.html
_templates/blocks/progress.html
_templates/blocks/quiz-buttons.html
_templates/blocks/quiz-buttons.html
_templates/util/debug_to_js.html
_templates/util/debug_to_js.html
_templates/util/var_dump.html
_templates/util/var_dump.html
```

### GAME APP
```
game/bots.py
game/constants.py
game/models.py
game/pages.py
game/tests.py
game/utils.py
game/templates/game/Congrats.html
game/templates/game/FinalResults.html
game/templates/game/Game.html
game/templates/game/Results.html
```

### 1. TRAINING / EXAMPLES / QUIZ APP

```
quiz/constants.py
quiz/models.py
quiz/pages.py
quiz/tests.py
quiz/utils.py
quiz/templates/quiz/Example1.html
quiz/templates/quiz/Example2.html
quiz/templates/quiz/Example3.html
quiz/templates/quiz/ExampleAll.html
quiz/templates/quiz/Examples.html
quiz/templates/quiz/GameIntro.html
quiz/templates/quiz/Intro1.html
quiz/templates/quiz/Intro2.html
quiz/templates/quiz/Intro3.html
quiz/templates/quiz/Intro4.html
quiz/templates/quiz/Intro5.html
quiz/templates/quiz/Intro6.html
quiz/templates/quiz/Intro7.html
quiz/templates/quiz/PracticeGame.html
quiz/templates/quiz/PracticeIntro.html
quiz/templates/quiz/PracticeResults.html
quiz/templates/quiz/Quiz1.html
quiz/templates/quiz/Quiz2.html
quiz/templates/quiz/Quiz3.html
quiz/templates/quiz/Quiz4.html
quiz/templates/quiz/Quiz.html
quiz/templates/quiz/ReviewGameRules.html
quiz/templates/quiz/blocks/examples-table.html
quiz/templates/quiz/forms/consent-form-student.html
quiz/templates/quiz/forms/consent-form-mturk.html
```

### 3. POST GAME SURVEY APP

```
survey/constants.py
survey/models.py
survey/pages.py
survey/tests.py
survey/templates/survey/Debriefing.html
survey/templates/survey/PostSurvey1.html
survey/templates/survey/PostSurvey2.html
survey/templates/survey/PostSurvey3.html
survey/templates/survey/PostSurvey4.html
```




### URL LIST

```
  APP / PAGE
---------------
 quiz / Intro1
 quiz / Intro2
 quiz / Intro3
 quiz / Intro4
 quiz / Intro5
 quiz / Intro6
 quiz / Intro7
 quiz / Examples
 quiz / Example1
 quiz / Example2
 quiz / Example3
 quiz / PracticeIntro
 quiz / PracticeGame1
 quiz / PracticeResults1
 quiz / PracticeGame2
 quiz / PracticeResults2
 quiz / Quiz
 quiz / Quiz1
 quiz / ReviewGameRules
 quiz / Quiz1
 quiz / Quiz2
 quiz / ReviewGameRules
 quiz / Quiz2
 quiz / Quiz3
 quiz / ReviewGameRules
 quiz / Quiz3
 quiz / Quiz4
 quiz / GameIntro
----------------
 game / Game
 game / ResultsWaitPage
 game / Results
 game / Game
 game / ResultsWaitPage
 game / Results
 game / Game
 game / ResultsWaitPage
 game / Results
 game / Game
 game / ResultsWaitPage
 game / Results
 game / Game
 game / ResultsWaitPage
 game / Results
 game / Game
 game / ResultsWaitPage
 game / Results
 game / Congrats
 game / FinalResults
 ----------------
 survey / PostSurvey1
 survey / PostSurvey2
 survey / PostSurvey3
 survey / PostSurvey4
 survey / Debriefing
```

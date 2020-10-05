# Variables needed for Treatment analysis Game



### Treatments

Experiment 1: 

1. Control group: Base Game
2. Treatment 1 (Control group 2): Descriptive Game
3. Treatment 2: Text Game

Experiment 2: 

1. Control group: Base Game
2. Treatment 1: Descriptive Game
3. Treatment 2: Enclosure Games



## Key variables

### Dependent variables (all individual level)



| Nr   | Variable name                | Construct    | Brief Description                                            | Data type |
| ---- | :--------------------------- | ------------ | ------------------------------------------------------------ | --------- |
| 1    | `mean_cont`                  | Contribution | an individual's average contribution through round r1 to r6  | FLOAT     |
| 2    | `cum_cont`                   | Contribution | an individual's cumulative contribution through round r1 and r6 | INTEGER   |
| 3    | `diff_r1_r2`                 | Change       | an individual's change of his/her contribution from round r1 to r2 | INTEGER   |
| 4    | `mean_diff_rounds`           | Change       | an individual's mean increase/decrease from round ri to ri+1 (with i=1 ...5) | FLOAT     |
| 5    | `mean_count_increase`        | Change       | the average number of rounds where an individual increases her/his contribution from round ri to ri+1 (with i=1 ...5) | FLOAT     |
| 6    | `mean_count_decrease/stable` | Change       | the average number of rounds where an individual decreases her/his contribution from round ri to ri+1 (with i=1 ...5) or remains stable | FLOAT     |
| 7    | diff_total                   | Change       | An individual's total change throughout the game measured as the \|max(contribution)- min(contribution)\| across all rounds r1 to r6 | INTEGER   |



### Co-variates

| Nr   | Variable name                | Brief Description                                            | Data type |
| ---- | :--------------------------- | ------------------------------------------------------------ | --------- |
| 8    | `rel_start_position`         | an individual's distance from the mean in round r1           | INTEGER   |
| 9    | `game-start`                 | the game's average contribution in round r1 (considering bots) | INTEGER   |
| 10   | `game_dynamics_r1_r2`        | the game's change in contribution from r1 to r2              | INTEGER   |
| 11   | `group_contribution_account` | The group's contribution account in round 6 in tokens        | INTEGER   |
| 12   | goal_met                     | Goal of 900 tokens achieved                                  | 0/1       |
| 13   | `group_contribution_r1`      | The group's contribution in round 1 (in %)                   | FLOAT     |
| 14   | `Social_dis`                 | A compound construct of cooperativenes (weighted average mean, after PCA and crombach's alpha analysis) | INTEGER   |
| 15   | `Environmental attitudes`    | Requires some PCA and cronbach's alpha analysis              | INTEGER   |

### Controls



| Nr   | Variable name             | Brief Description                               | Data type |
| ---- | :------------------------ | ----------------------------------------------- | --------- |
| 8    | `a`ge                     |                                                 | INTEGER   |
| 9    | `g`ender                  |                                                 | FACTOR    |
| 10   | `economic status`         |                                                 | FACTOR    |
| 11   | `political situation`     |                                                 | FACTOR    |
| 12   | `prior game experience`   |                                                 | 0/1       |
| 15   | `Environmental attitudes` | Requires some PCA and cronbach's alpha analysis | INTEGER   |



## Additional variables needed



| Nr   | Variable name  | Brief Description                                            | Data type |
| ---- | :------------- | ------------------------------------------------------------ | --------- |
| 8    | `user_id`      |                                                              | STRING    |
| 9    | `treatment_id` | 1=Base Game, 2=Descriptive Text Game v 1.1., 3=Injunctive Text Game, 4=Visualization Game (Enclosure) | FACTOR    |



## DEA ANALYSIS ## (Design of Experiment Analysis)

* Data inspections
  * Are there entries suggesting low quality (e.g. age out of range, e.g. all values the same 10,10,10,10)
* Creating the descriptives for the dependent variables (see above)
* Creating one data frame with all games and a treatment_id
* Creating basic statistics on this variables
  * Mean, median, min, max, std, 
  * Plotting a box plots to see if confidence intervals overlap on means
  * simple t-test
* Preparing an Anova
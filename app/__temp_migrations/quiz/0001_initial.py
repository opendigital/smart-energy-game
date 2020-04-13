# Generated by Django 2.2.4 on 2020-04-08 04:54

from django.db import migrations, models
import django.db.models.deletion
import otree.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('otree', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_in_subsession', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_group', to='otree.Session')),
            ],
            options={
                'db_table': 'quiz_group',
            },
        ),
        migrations.CreateModel(
            name='Subsession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('session', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quiz_subsession', to='otree.Session')),
            ],
            options={
                'db_table': 'quiz_subsession',
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_in_group', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('_payoff', otree.db.models.CurrencyField(default=0, null=True)),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('_gbat_arrived', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, null=True)),
                ('_gbat_grouped', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, null=True)),
                ('quiz_data', otree.db.models.LongStringField(null=True)),
                ('quiz_bonus', otree.db.models.IntegerField(default=0, null=True)),
                ('review_rules', otree.db.models.IntegerField(default=0, null=True)),
                ('practice_contrib1', otree.db.models.CurrencyField(null=True)),
                ('practice_contrib2', otree.db.models.CurrencyField(null=True)),
                ('q1', otree.db.models.IntegerField(choices=[[1, '2 tokens'], [2, '3 tokens'], [3, '6 tokens'], [4, '11 tokens']], null=True, verbose_name='On average, how many tokens will each player need to invest into the group conservation account in each round in order to meet the 60% group conservation goal')),
                ('q2', otree.db.models.BooleanField(choices=[[1, 'True'], [0, 'False']], null=True, verbose_name='For each energy token in the group conservation account $0.01 is contributed to Carbonfund.org to reduce actual air pollution in the real world')),
                ('q3a', otree.db.models.BooleanField(choices=[[1, 'True'], [0, 'False']], null=True, verbose_name='You will have greater earnings than others if you put all of your energy tokens in your private account, while others contribute all of theirs to the group conservation account')),
                ('q3b', otree.db.models.BooleanField(choices=[[1, 'True'], [0, 'False']], null=True, verbose_name='True or False: The group will maximize its earning if all players contribute 6 of their energy tokens to the group conservation account each month')),
                ('q4a', otree.db.models.IntegerField(choices=[[1, '$0.00'], [2, '$0.30'], [3, '$3.00']], null=True, verbose_name='My payout from my private account is')),
                ('q4b', otree.db.models.IntegerField(choices=[[1, '$0.72'], [2, '$1.00'], [3, '$2.72']], null=True, verbose_name='My bonus payout from the group conservation account is')),
                ('q4c', otree.db.models.IntegerField(choices=[[1, '$0.50'], [2, '$1.02'], [3, '$3.72']], null=True, verbose_name='Total payout is (private plus group conservation bonus)')),
                ('q4d', otree.db.models.IntegerField(choices=[[1, '$0.00'], [2, '$0.30'], [3, '$3.00']], null=True, verbose_name='My payout from my personal account is')),
                ('q4e', otree.db.models.IntegerField(choices=[[1, '$0.00'], [2, '$1.00'], [3, '$2.00']], null=True, verbose_name='My payout from the group conservation account is')),
                ('q4f', otree.db.models.IntegerField(choices=[[1, '$0.00'], [2, '$0.30'], [3, '$3.00']], null=True, verbose_name='Total payout is (private plus group conservation bonus)')),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.Group')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_player', to='otree.Participant')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_player', to='otree.Session')),
                ('subsession', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Subsession')),
            ],
            options={
                'db_table': 'quiz_player',
            },
        ),
        migrations.AddField(
            model_name='group',
            name='subsession',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Subsession'),
        ),
    ]

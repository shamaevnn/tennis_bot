# Tennis Telegram Bot

## Problem
Tennis coach had several problems:
 * All participants of training process had to inform coach that they will miss a coming training.
 * If the student wanted to sign up for a training session, he had to ask the coach if this lesson was available and if it was possible to come. So, the coach had to look in his paper schedule and look for free places.
 * All group students have `bonus lesson` — opportunity to visit a lesson for free. Coach had to track the number of these bonuses!!!
 * These and other not described problems detracted coach from training process.

## Solution
For solving these and others not stated problems, *tennis bot* was created.
**Actually, there are two bots: bot for coach and bot for players.**

Functionality of coach bot:
 * [Viewing schedule](./docs/COACH_BOT.md#schedule)
 * [Checking payments](./docs/COACH_BOT.md#payment-info)
 * [Sending message to players](./docs/COACH_BOT.md#sending-message)

Functionality of player's bot:
 * [Checking my info](./docs/PLAYER_BOT.md#my-info)
 * [Taking a lesson](./docs/PLAYER_BOT.md#taking-a-training-individual-or-group)
 * Rent court
 * [Skipping a lesson](./docs/PLAYER_BOT.md#taking-a-training-individual-or-group)


## Used technologies
This bot was built based on [django-telegram-bot](https://github.com/ohld/django-telegram-bot)
 * `Python` 🐍
 * `Django` 🦾 for its admin panel
 * `Dokku` + `GitHub Actions` 🧠 for auto-deploy
 * `PostgreSql` 💾

## Summary
This bot helps to automate routine tasks of the coach. With this bot, he doesn't have to manually track a lot of information from about 100 people and spend his time on this during trainings. 

## [Contributing](./CONTRIBUTING.md)

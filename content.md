---
layout: post
title:  "The role of assurance contracts in protest movements"
date:   2026-11-04
permalink: /
---

Voicing disapproval is very important.
Naively one might think that if something is unpopular, impactful, and raises people's passion then people would express their disapproval and a mass movement would form.
It's clear from the past decade that it's not so linear.
The Trump administration did things on a regular basis that large majorities dissapproved of passionately, and yet mass movements only occurred sporadically.

There are ``professional protesters'' who can always be relied upon to express their views.
However, the majority of American's are not professional protesters, nor should they be held to that standard.
For us normies there is a cost to going to a protest (primarly in time, but also money if you need to hire childcare).
Moreover, going to a protest is only worth the cost for an individual if the decision turns a failing protest into a successful one (if the protest is already successful you can free-ride). The protest is only successful if a lot of other normies go to it.  So the decision to go to a protest for a group of individuals feels like a prisoner's dillemma.

It's technically not well modeled by a prisoner's dillemma.  It's really more a combination of two other games

1. Chicken
2. Stag Hunt

In this note I'll go through both these games briefly.  We will see how in these games, going to a protest is not really rational.

At the end I'll propose a solution, that changes the games so that going to a protest is rational.

# Chicken
The original game of chicken was inspired by idiot teenagers who would drive their cars towards a cliff.  The first car to swerve is the loser.  There are three outcomes:
 - both cars swerve (both idiots lose)
 - one car swerve (one idiot wins and the other loses)
 - neither swerve (both idiots crash and die)

There are 2 pure Nash equilibria (just one car swerves).  The conclusion I draw is that in games of chicken, rationality is not a thing.
**There is no purely rational action we can expect a player to take.**

We have the same dynamic going on when we launch protest movements.
In order for activists to be successful, they need to mobilize a portion of the population (maybe 3%).  Let's assume everybody benefits from a successful protest.
However, only the protesters pay the cost of protesting.
Even if the cost is low, the "game" of going to a protest is isomorphic to an $N$ person game of chicken where we need a small minority to make a sacrifice that benefits everybody.
Since Chicken does not have a unique Nash equilibria, we can not expect people to "wise-up" and be heroes.  Just because the outcome of a massive protest might benefit us all does not make it rational for an individual to attend a protest.

# Stag Hunt
I personally do not like to go to a party unless I know some of my friends will be there. I can imagine a similar obstacle to going to protest. Without coordinating, this puts me and my friends in a situation described by a game called "Stag Hunt".

In stag hunt we have two hunters in a forrest of deer and squirrels.  The hunters can cooperate and get a deer together.  However, either of the hunter can ``defect'' and go after a squirrel by themself.  Again there are three outcomes:

 - both hunters cooperate and get a stag (big win for both)
 - both hunters defect and get squirrells (small win for both)
 - one hunter defects while the other intended to cooperate (the defector gets a small win, the other hunter gets nothing)

Again, there are two pure Nash equilibria.  Both hunters cooperate, and both hunters defect.  In any case, rational behavior is not enough to determine the outcome.

And again, this models another dynamic that exists when a protest is launched.
When somebody considers whether or not to go to a protest, it's only worth going if lots of other people go. I wont belabor the point further, except to say that there are now two games that model going to protests, and both of them suggest that going to a protest that benefits you is not exactly rational.

# How to make protests rational
Our goal is to setup a system where protesting (for just causes) is rational, and so we should look at the circumstances that lead to games like chicken and stag-hunt (so that we may avoid them).

The biggest assumption that we can tweak is the notion that all the players act independently of each other.  In other words, we need to build a coordination mechanism.  This coordination mechanism should be one where individuals to benefit from a protest will volunteer to attend that protest.

The simplest coordination mechanism I've seen is called an assurance contract. This would be roughly waht the assurance contract looks like in the context of protests

> I, Larry, will attend the protest on March 25th if there are at least 200 other attendees and at least 3 people from the following list also attend: 
> - Alice
> - Bob
> - Carl
> - Danielle
> - Edwin
> 
> If these conditions are not met by March 24th at 10:00am PST, then this contract is void. Violation of the contract carries a fine of $1.00

This contract addresses both stag-hunt and chicken because

1. There is no risk of going to a protest that is too small (it's hardcoded in the contract).  This bypasses the chicken game.
2. There is no risk of going to a protest without my friends.  This bypasses the stag-hunt game.

The assurance contract does not allow us to escape game theory though, because now there is a new decision.  Each individual must decide to sign or not sign a contract. However, in this case the Nash equilibria is to sign the contract because there are only two possibilities.  Either there will be enouth signees and the protest will be large enough to be deemed a success, or the will not be enough signees and the protest will simply not happen.  There is no risk of a small unsuccessful protest (because the contract goes void before that happens), and there is no risk of being there without your friends.  So there is no cost to signing the contract.  This is a trivial game where the Nash equilibria is to sign an assurance contract.

This might seem like a very small tweak.  However, I think this has the potential to be sneakily big in that this method of building a protest movement will scale through a network and allow small things to become large.

# Cascade Phenomena

Each citizen is a node in a social network.  As a simulation we could imagine citizens floating assurance contracts where they agree to go to a protest if 10\% of the population attends and a majority of their friends attend.
Under normal circumstances this never happens.  However, if you have a server that coordinates all these assurance contracts then small movements bubble up into large ones frequently

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

# Chicken and the free-rider problem
Those of us who may disapprove of a policy might want to protest, but at the same time we realize that a single individual is not enough to make a difference.  The protest needs to be large.  Perhaps 5% of the population.  There is no point in going to a protest that is too small.
At the same time, we do not need 90% percent of the population to make a difference.  If the protest has 10% of the population, that is plenty large, and going to it will also not be rational.  So if you have other personal things pulling you, it's sensible to rely on others to shoulder the weight of going to protests.

This is an instance of the free-rider problem.
Just for color, it's fun to consider the free-rider problem when there are only two people.  In this instance the game is called "chicken".  This was a game played by idiot teenagers in the 1950s who would drive their cars towards a cliff.  The first car to swerve is the loser.  There are three outcomes:
 - both cars swerve (both idiots lose)
 - one car swerve (one idiot wins and the other loses)
 - neither swerve (both idiots crash and die)

There are 2 pure Nash equilibria (just one car swerves).  When there are multiple Nash equilibria rationality is not a thing.  We have a coordination problem.
**There is no purely rational action we can expect a player to take.**

We have the same dynamic going on when we launch protest movements.
Even if the cost is low, the "game" of going to a protest is isomorphic to an $N$ person game of chicken where we need a small minority to make a sacrifice that benefits everybody.
Since free-rider problems do not have unique Nash equilibria, we can not expect people to "wise-up" and be heroes.  Just because the outcome of a massive protest benefits us all does not make it rational to protest.

# Stag Hunt
The other dynamic I see at protests is that for "normies" it is not unlike going to a party where you may or may not have any friends. I personally do not like to go to a party unless I know some of my friends will be there. Without coordinating, this puts me and my friends in a situation described by a game called "Stag Hunt".

In stag hunt we have two hunters in a forrest of deer and squirrels.  The hunters can cooperate and get a deer together.  However, either of the hunter can ``defect'' and go after a squirrel by themself.  Again there are three outcomes:

 - both hunters cooperate and get a stag (big win for both)
 - both hunters defect and get squirrells (small win for both)
 - one hunter defects while the other intended to cooperate (the defector gets a small win, the other hunter gets nothing)

Again, there are two pure Nash equilibria.  Both hunters cooperate, and both hunters defect.  In any case, rational behavior is not enough to determine the outcome.

And again, this models another dynamic that exists when a protest is launched.
When somebody considers whether or not to go to a protest, it's only worth going if they do not feel isolated from their group. 

I wont belabor the point further, except to say that there are now two games that model going to protests, and both games suggest that going to a protest that benefits everybody is not exactly rational.
We can grumble about this, and I did that for a long time.  However, I think there is a solution.


# How to make protests rational
Here is the dumbest solution.  It's called an assurance contract. This would be roughly what the assurance contract looks like in our context

> I, Larry, will attend protest X on March 25th if there are at least 2000 other attendees and at least 3 people from the following list also attend: 
> - Alice
> - Bob
> - Carl
> - Danielle
> - Edwin
> 
> If these conditions are not met by March 24th at 10:00am PST, then this contract is void. Violation of the contract carries a fine of $1.00

This contract addresses both stag-hunt and chicken because

1. There is no risk of going to a protest that is too small (it's hardcoded in the contract).  This bypasses the free-rider problem.
2. There is no risk of going to a protest without my friends.  This bypasses the stag-hunt game.

Lastly, there is no risk to signing the contract because if you sign the contract there are only two outcomes:

1. The contract is triggered, and Larry + his friends to to a protest that is large enough to be worth the time.
2.  The contract is not triggered, and Larry is no worse off than he was before.

The game theory in a world of assurance contracts is trivial. Each individual must decide to sign or not sign a contract. However, in this case the Nash equilibria is to sign the contract because the contract has no downside risk relative to the status quo. Thus there is a unique Nash equilibria, and "rational" is now well defined.  It is now rational to sign the assurance contract and go to a protest if the oppurtunity arises.

This might seem like a very small tweak.  However, I think this has the potential to be sneakily big. At this point it's easier to show rather than tell.

# Cascade Phenomena

Each citizen is a node in a social network.  As a simulation we could imagine citizens floating assurance contracts where they agree to go to a protest if 10\% of the population attends and a majority of their friends attend.
Under normal circumstances this never happens.  However, if you have a server that coordinates all these assurance contracts then small movements bubble up into large ones frequently

<video controls loop muted playsinline width="100%">
  <source src="{{ '/simulation/grid_protest.mp4' | relative_url }}" type="video/mp4">
  Your browser does not support the video tag.
</video>


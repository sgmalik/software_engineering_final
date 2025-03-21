## hand_evaluator 
the HandEvaluator class provides information on the strength of a poker hand. 

To use HandEvaluator you would call the hand_eval function like so: 
```
hand_info = HandEvaluator.hand_eval(hole_cards, community_cards)
```
You would then get an object like this: 
```
{
    "strength": {
        "hand_rank": Int,
        "primary_cards_rank": []
    },
        "kickers": []
}
```
hand_rank: the rank of the hand given (Ex. high_card, pair, two pair, etc). This is on a 1-10 scale (high_card being 1, royal_flush being a 10)

primary_cards_rank: these are used for tie breaking the same hand_rank, Ex. the hand is a pair of 2's.
```
hand_info["strength"]["primary_cards_rank"] = [2]
```

kickers: the kickers are also used for tie-breaking, these are the highest ranked individual cards (2-14) that aren't used in hand_rank or primary_cards_rank 
## game_evaluator
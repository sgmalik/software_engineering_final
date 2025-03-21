# git workflow 
1. Start from main, and create a new branch named with the feature you're working on. 
```
git checkout -b <feature_name>
```
2. Once done test your code (using pytest) Ex. test_feature.py 
```
class TestFeature():
 
    def test_some_function(self):
        """
        example test 
        """
        
        assert func_output = expected_output 
```
3. Run pylint on newly created code (appease Jason)
```
Running pylint examples 

pylint feature.py
pylint src
pylint src/feature.py 

```
4. Once code is tested, and checked for good syle merge to main
```
git checkout main 
git merge <feature_name>
```
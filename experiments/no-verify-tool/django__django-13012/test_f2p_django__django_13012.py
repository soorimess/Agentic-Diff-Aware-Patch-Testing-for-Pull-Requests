"""
Test for Django issue: Constant expressions of an ExpressionWrapper 
object are incorrectly placed at the GROUP BY clause.
"""
# This will be run as a basic Python script to verify the behavior


def test_expression_wrapper_group_by_behavior():
    """
    Test that demonstrates the key behavior difference.
    
    Before fix: ExpressionWrapper(Value(3)).get_group_by_cols() returns [wrapper]
    After fix:  ExpressionWrapper(Value(3)).get_group_by_cols() returns [] 
    """
    # Note: This test works in the context where Django is already properly available
    from django.db.models import Value, IntegerField, ExpressionWrapper
    
    # Create the problematic scenario
    expr = Value(3, output_field=IntegerField())
    expr_wrapped = ExpressionWrapper(expr, output_field=IntegerField())
    
    # The specific behavior we're testing
    group_by_cols = expr_wrapped.get_group_by_cols()
    
    # Demonstrate the bug with assertion that will fail before fix
    assert len(group_by_cols) == 0, (
        f"BUG CONFIRMED: ExpressionWrapper incorrectly places constant in GROUP BY.\n"
        f"Expected empty list, got: {group_by_cols}\n"
        f"This causes PostgreSQL errors when querying with constant expressions in GROUP BY."
    )
    
    print("SUCCESS: ExpressionWrapper properly excludes constants from GROUP BY")
    return True


def main():
    """Main function to run the test"""
    try:
        test_expression_wrapper_group_by_behavior()
        print("Test passed successfully!")
        return True
    except AssertionError as e:
        print(f"Test failed as expected (bug present): {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


if __name__ == "__main__":
    main()
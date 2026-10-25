# Contributing to PromptLab

Thanks for taking a look. Small, focused contributions are welcome.

## Good first contributions

- Add a prompt example for a real developer task.
- Improve an error message or edge-case test.
- Add documentation showing a clear workflow.
- Suggest a feature with a small, concrete use case.

## Before opening a pull request

1. Explain the problem and expected behavior.
2. Keep changes focused and avoid adding dependencies without a clear reason.
3. Run the tests:

   ```bash
   python -m unittest discover -s projects/promptlab -p 'test_*.py' -v
   ```

4. Do not include API keys, passwords, access tokens, customer data, or confidential prompts in commits or issues.
5. For new prompt examples, use fictional/sample inputs and explain the intended task.

Please be respectful in review and open to feedback.

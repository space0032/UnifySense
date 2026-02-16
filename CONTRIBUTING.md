# Contributing to UnifySense

We welcome contributions to the UnifySense Clinical Diagnosis Assistant! This document provides guidelines for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:
- Be respectful and inclusive
- Focus on constructive feedback
- Prioritize patient safety and data privacy
- Follow medical ethics guidelines

## How to Contribute

### Reporting Bugs

1. Check existing issues to avoid duplicates
2. Use the bug report template
3. Include:
   - Clear description of the issue
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details
   - Screenshots if applicable

### Suggesting Enhancements

1. Check existing feature requests
2. Clearly describe the enhancement
3. Explain the use case and benefits
4. Consider medical/clinical validity

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Write/update tests
5. Update documentation
6. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
7. Push to the branch (`git push origin feature/AmazingFeature`)
8. Open a Pull Request

## Development Guidelines

### Code Style

**Python (Backend):**
- Follow PEP 8
- Use type hints
- Document functions with docstrings
- Maximum line length: 100 characters

**TypeScript (Frontend):**
- Follow Airbnb style guide
- Use functional components
- Implement proper TypeScript types
- Use meaningful variable names

### Testing

- Write unit tests for new features
- Maintain test coverage above 80%
- Test edge cases and error conditions
- Include integration tests for API endpoints

### Documentation

- Update README.md for significant changes
- Document API changes in API_DOCUMENTATION.md
- Include inline comments for complex logic
- Update architecture diagrams if needed

### Medical Safety

- **Critical**: All medical-related changes must be reviewed by healthcare professionals
- Never remove safety warnings or disclaimers
- Validate medical logic against evidence-based guidelines
- Consider edge cases and failure modes

### Commit Messages

Follow conventional commits:
```
feat: add symptom severity visualization
fix: correct ICD-10 code mapping
docs: update API documentation
test: add unit tests for diagnosis service
refactor: optimize Bedrock service calls
```

### Branch Naming

- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions/modifications

## Project Structure

```
UnifySense/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── models/       # Data models
│   │   ├── services/     # Business logic
│   │   └── utils/        # Utilities
│   ├── tests/            # Backend tests
│   ├── main.py           # Application entry
│   └── requirements.txt  # Dependencies
├── frontend/
│   ├── public/           # Static files
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API services
│   │   └── types/        # TypeScript types
│   └── package.json      # Dependencies
└── docs/                 # Documentation
```

## Setting Up Development Environment

1. **Clone the repository**:
   ```bash
   git clone https://github.com/space0032/UnifySense.git
   cd UnifySense
   ```

2. **Backend setup**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Frontend setup**:
   ```bash
   cd frontend
   npm install
   ```

4. **AWS Configuration**:
   - Set up AWS credentials
   - Enable Bedrock access
   - Configure environment variables

## Review Process

1. All PRs require at least one review
2. CI/CD checks must pass
3. Medical-related changes need clinical review
4. Maintain backward compatibility
5. Update version numbers appropriately

## Medical Disclaimer

This project is for educational and assistive purposes. All contributions must:
- Include appropriate medical disclaimers
- Not claim to replace professional medical judgment
- Follow evidence-based medical practices
- Respect patient privacy and data protection

## Questions?

- Open an issue for questions
- Join discussions in existing issues
- Contact maintainers directly for sensitive matters

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (see LICENSE file).

Thank you for contributing to UnifySense!

# Contributing to Sleepwalker Protocol (SWP)

Thank you for your interest in contributing to the Sleepwalker Protocol! This project exists to strengthen emotional safety in human-AI interactions, and we welcome contributions that advance this mission.

## Guiding Principles

**"Nothing About Us Without Us"**

This project is governed by those with lived experience of neurodivergence, mental health conditions, and the protective psychological states that SWP addresses.

### Our Values

- **Lived Experience Leadership** - Those with direct experience guide development priorities
- **Trauma-Informed Design** - Safety, consent, and user control are non-negotiable
- **Evidence-Based** - Clinical research and user feedback inform all decisions
- **Open Source Forever** - Community benefit over commercial interests

## Ways to Contribute

### 1. User Experience Reports

**Most Valuable Contribution:** Tell us how SWP works (or doesn't work) for you.

- Share scenarios where SWP improved your AI interactions
- Report situations where AI systems violated SWP principles
- Describe edge cases we haven't considered
- Provide feedback on protocol clarity and usability

**How to submit:**
- Open a GitHub issue with the label `user-experience`
- Anonymous submissions welcome via email: haief@neuroliftsolutions.com

### 2. Clinical Expertise

We seek contributions from mental health professionals, trauma-informed care practitioners, and researchers:

- Review protocol alignment with clinical best practices
- Suggest evidence-based improvements
- Provide academic citations supporting protocol elements
- Identify potential harms we haven't addressed

**How to submit:**
- Open a GitHub issue with the label `clinical-review`
- Include relevant credentials and research citations

### 3. Technical Implementation

Code contributions are welcome for:

- Core protocol implementation (Python, JavaScript/TypeScript)
- Integration libraries for popular AI frameworks
- Testing and validation tools
- Documentation improvements
- Bug fixes

**How to submit:**
- Fork the repository
- Create a feature branch
- Submit a pull request with clear description
- Ensure all tests pass

### 4. Research Collaboration

Academic researchers interested in studying SWP effectiveness:

- Propose validation studies
- Share research findings
- Collaborate on academic publications
- Contribute to evidence base

**How to submit:**
- Email research proposals to: haief@neuroliftsolutions.com
- Open GitHub discussion for community input

## Development Guidelines

### Setting Up Development Environment

**Python:**
```bash
git clone https://github.com/NeuroLift-Technologies/sleepwalker.git
cd sleepwalker
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

**JavaScript/Node.js:**
```bash
git clone https://github.com/NeuroLift-Technologies/sleepwalker.git
cd sleepwalker
npm ci
```

`package-lock.json` is committed for reproducible Node installs. Use
`npm install` only when intentionally changing dependencies and committing the
resulting lockfile update.

### Running Tests

**Python:**
```bash
python3 -m pytest tests/
```

**JavaScript/TypeScript:**
```bash
npm run build
npm test
npm pack --dry-run
```

The TypeScript package builds from `src/` into `dist/`; `dist/` is ignored and
should not be committed. `prepublishOnly` runs `npm run build`, so a dry-run
pack is the closest local check for publish readiness. The npm package is
published as `@neurolift-technologies/sleepwalker-protocol@1.0.0`, and
`publishConfig.access` is `public`; if release metadata changes, confirm
`npm publish --dry-run` reports the scoped package name and public access before
publishing.

**Governance docs and templates:**
```bash
bash .nltotoi/scripts/validate-governance.sh
```

At present, `.github/workflows/validate-governance.yml` is the only tracked CI
workflow in this repository. Run Python and TypeScript checks locally when those
surfaces change.

### Code Style

**Python:**
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Maximum line length: 100 characters
- Run `black` and `flake8` before committing

**JavaScript/TypeScript:**
- Follow standard JavaScript style guide
- Use ESLint and Prettier
- Prefer TypeScript for new code
- Include JSDoc comments for public APIs

### Commit Messages

Human-authored commits should use conventional commits:

```
type(scope): brief description

Longer explanation if needed

Closes #issue-number
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `chore`: Maintenance tasks

Coding-agent commits must follow the OTOI agent format:

```
[AGENT_NAME] type(scope): description
```

### Pull Request Process

1. **Fork and Branch**
   - Fork the repository
   - Create a descriptive branch name: `feat/add-dissociation-detection` or `fix/consent-check-bug`

2. **Make Changes**
   - Write clear, focused commits
   - Add tests for new functionality
   - Update documentation as needed
   - Ensure all tests pass

3. **Submit PR**
   - Provide clear description of changes
   - Link related issues
   - Explain the "why" behind changes, not just "what"
   - Request review from maintainers

4. **Review Process**
   - Maintainers will review within 1 week
   - Address feedback and requested changes
   - Once approved, maintainer will merge

## Community Standards

### Code of Conduct

We are committed to providing a welcoming, safe, and inclusive environment:

- **Be Respectful** - Treat all contributors with dignity
- **Be Inclusive** - Welcome diverse perspectives and experiences
- **Be Patient** - Remember that many contributors have disabilities or mental health conditions
- **Be Constructive** - Provide helpful feedback
- **Assume Good Intent** - Give others benefit of the doubt

### Unacceptable Behavior

- Harassment, discrimination, or hate speech
- Dismissing lived experiences of neurodivergent individuals
- Pressuring contributors to share personal mental health information
- Trolling, inflammatory comments, or personal attacks
- Privacy violations or doxxing

**Reporting:** Contact haief@neuroliftsolutions.com or open a private issue.

## Governance

### Decision-Making

Major decisions are made by:

1. **Neurodivergent Advisory Council** - Lived experience leadership (final say)
2. **Clinical Advisory Board** - Evidence-based recommendations
3. **Technical Maintainers** - Implementation feasibility
4. **Community Input** - Open discussion on GitHub

### Quarterly Updates

Protocol updates are released quarterly based on:
- User feedback and experience reports
- New clinical research findings
- Technical improvements
- Community proposals

## Recognition

All contributors are acknowledged in:
- CONTRIBUTORS.md file
- Release notes for their contributions
- Academic publications citing community input

We value all contributions equally - user experience reports are just as important as code contributions.

## Questions?

- **General Questions:** Open a GitHub discussion
- **Private Inquiries:** haief@neuroliftsolutions.com
- **Technical Issues:** Open a GitHub issue with appropriate label

## License

By contributing, you agree that your contributions will be licensed under the
terms that apply to this repository and the package manifest you are changing.
See [LICENSE](LICENSE) before submitting changes.

---

**Thank you for helping make AI interactions emotionally safer for everyone.**

**Built with lived experience. Governed by community. Open source forever.**

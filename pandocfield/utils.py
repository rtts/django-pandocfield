import subprocess

def pandoc(source):
    p = subprocess.Popen(['pandoc', '--smart', '--mathjax'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # something else than 'None' indicates that the process already terminated
    if not (p.returncode is None):
        raise RuntimeError('Pandoc died with exitcode {} before receiving input: {}'.format(p.returncode, p.stderr.read()))

    try:
        source = source.encode('utf-8')
    except UnicodeEncodeError:
        # assume that it is already a utf-8 encoded string
        pass

    stdout, stderr = p.communicate(source)

    try:
        stdout = stdout.decode('utf-8')
    except UnicodeDecodeError:
        raise RuntimeError('Pandoc output was not utf-8. Weird.')

    if p.returncode != 0:
        raise RuntimeError('Pandoc died with exitcode {} during conversion: {}'.format(p.returncode, stderr))

    return '<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>' + stdout

"""
Diagnóstico do áudio por idioma do Blind Tube.

Compara o áudio padrão (formato 18, como o programa faz hoje) com o áudio
dublado (m4a) de um idioma, usando a mesma biblioteca de som do programa.

Uso, a partir da pasta blind_tube (onde estão yt-dlp.exe e cookies.txt):

    ..\\venv\\Scripts\\python ..\\tools\\diagnostico_audio.py "LINK_DO_VIDEO" pt > diagnostico-audio.txt 2>&1
"""
import subprocess
import sys
import time
import traceback
from urllib.parse import urlparse, parse_qs

import requests
from sound_lib import output, stream
from sound_lib.effects import Tempo


def p(*args):
    print(*args, flush=True)


def get_url(video_url, format_selector, extra_args=()):
    cmd = ["yt-dlp", "-g", "-f", format_selector, "--cookies", "cookies.txt",
           "-R", "5", *extra_args, video_url]
    p("comando:", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True,
                            encoding="utf-8", errors="replace", timeout=120)
    p("yt-dlp saiu com codigo", result.returncode)
    if result.stderr.strip():
        p("yt-dlp stderr:", result.stderr.strip()[:800])
    lines = [l.strip() for l in result.stdout.splitlines() if l.strip().startswith("http")]
    return lines[0] if lines else None


def describe_url(url):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    p("host:", parsed.netloc)
    for key in ("itag", "mime", "dur", "clen", "sabr", "c", "ratebypass"):
        if key in query:
            p(f"  {key} = {query[key][0]}")
    p("tamanho da URL:", len(url), "caracteres")


def probe_http(url):
    try:
        response = requests.get(url, headers={"Range": "bytes=0-99"},
                                stream=True, timeout=30)
        p("HTTP status:", response.status_code)
        p("HTTP content-type:", response.headers.get("Content-Type"))
        p("HTTP content-range:", response.headers.get("Content-Range"))
        first = next(response.iter_content(64), b"")
        p("primeiros bytes:", first[:32])
        response.close()
    except Exception:
        p("HTTP falhou:")
        p(traceback.format_exc())


def play_test(label, factory, seconds=6):
    p(f"--- {label} ---")
    try:
        handle = factory()
    except Exception:
        p("FALHOU ao criar o stream:")
        p(traceback.format_exc())
        return
    try:
        try:
            p("bytes totais:", len(handle))
        except Exception as e:
            p("len() falhou:", e)
        try:
            p("duracao (s):", round(handle.length_in_seconds(), 1))
        except Exception as e:
            p("length_in_seconds falhou:", e)
        handle.play()
        for i in range(seconds):
            time.sleep(1)
            try:
                position = round(handle.bytes_to_seconds(), 1)
            except Exception:
                position = "?"
            p(f"  t={i + 1}s posicao={position}s tocando={handle.is_playing} travado={handle.is_stalled}")
        handle.stop()
    except Exception:
        p("erro durante a reproducao:")
        p(traceback.format_exc())
    finally:
        try:
            handle.free()
        except Exception:
            pass


def main():
    if len(sys.argv) < 2:
        p("Uso: diagnostico_audio.py LINK [codigo_do_idioma]")
        return
    video_url = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else "pt"
    output.Output()

    p("=== PADRAO: formato 18, cliente android (como o programa faz hoje) ===")
    url18 = get_url(video_url, "18", ("--extractor-args", "youtube:player_client=android"))
    if url18:
        describe_url(url18)
        probe_http(url18)
        play_test("formato 18 (Tempo + decode, como o programa)",
                  lambda: Tempo(stream.URLStream(url18, decode=True)))
    else:
        p("nao foi possivel obter a URL do formato 18")

    p()
    p(f"=== DUBLADO: m4a em '{language}', cliente padrao ===")
    url_dub = get_url(video_url, f"ba[ext=m4a][language={language}]")
    if url_dub:
        describe_url(url_dub)
        probe_http(url_dub)
        play_test("m4a dublado (Tempo + decode, como o programa)",
                  lambda: Tempo(stream.URLStream(url_dub, decode=True)))
        play_test("m4a dublado (stream simples, sem decode)",
                  lambda: stream.URLStream(url_dub))
    else:
        p("nao foi possivel obter a URL do m4a dublado")
    p()
    p("fim do diagnostico")


if __name__ == "__main__":
    main()

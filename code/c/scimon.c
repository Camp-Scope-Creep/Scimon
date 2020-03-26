/*******************************************************************************
 * Ohhhh Scimon. The old 1978 game is born again with tiny computers and double
 * the play surface. And for a bonus, this app will throw in an "musical instrument
 * mode".
 ******************************************************************************/
#ifdef HAVE_CONFIG_H
#include <config.h>
#endif
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <fcntl.h>
#include <pulse/simple.h>
#include <pulse/error.h>

#include <stdlib.h>
#include <sys/types.h>
#include <dirent.h>




void loadsoundFileInfos() {
    DIR* FD;
    struct dirent* soundFileInfo;
    FILE    *soundFile;
    char    buffer[BUFSIZ];

    // Scan the sample directory
    if (NULL == (FD = opendir ("samples/"))) {
        fprintf(stderr, "Error : Failed to open input directory - %s\n", strerror(errno));
        fclose(common_file);

        return 1;
    }

    while ((soundFileInfo = readdir(FD))) {
        /* On linux/Unix we don't want current and parent directories
         * On windows machine too, thanks Greg Hewgill
         */
        if (!strcmp (soundFileInfo->d_name, "."))
            continue;
        if (!strcmp (soundFileInfo->d_name, ".."))    
            continue;
        /* Open directory entry file for common operation */
        /* TODO : change permissions to meet your need! */
        soundFile = fopen(soundFileInfo->d_name, "r");
        if (soundFile == NULL) {
            fprintf(stderr, "Error : Failed to open sound file - %s\n", strerror(errno));
            fclose(common_file);

            return 1;
        }

        // Load the data in the file into PulseAudio sample

        pa_stream* pa_stream_new    (   pa_context *    c,
        const char *    name,
        const pa_sample_spec *  ss,
        const pa_channel_map *  map 
)   


        /* Doing some struf with soundFile : */
        /* For example use fgets */
        while (fgets(buffer, BUFSIZ, soundFile) != NULL)
        {
            /* Use fprintf or fwrite to write some stuff into common_file*/
        }

        /* When you finish with the file, close it */
        fclose(soundFile);
    }

    /* Don't forget to close common file before leaving */
    fclose(common_file);

    return 0;
}




//////////////////////////////////////////////////////
#define BUFSIZE 1024
int main(int argc, char*argv[]) {

    setenv("PULSE_PROP_application.name", _("Scimon"), 1);

    // The Sample format to use
    static const pa_sample_spec ss = {
        .format = PA_SAMPLE_S16LE,
        .rate = 44100,
        .channels = 2
    };
    pa_simple *s = NULL;
    int ret = 1;
    int error;


    // -------------------- Audio Init -------------------------
    // Open a connection to PulseAudio
    _context =  












    /* replace STDIN with the specified file if needed */
    if (argc > 1) {
        int fd;
        if ((fd = open(argv[1], O_RDONLY)) < 0) {
            fprintf(stderr, __FILE__": open() failed: %s\n", strerror(errno));
            goto finish;
        }
        if (dup2(fd, STDsoundFileInfoNO) < 0) {
            fprintf(stderr, __FILE__": dup2() failed: %s\n", strerror(errno));
            goto finish;
        }
        close(fd);
    }

    /* Create a new playback stream */
    if (!(s = pa_simple_new(NULL, argv[0], PA_STREAM_PLAYBACK, NULL, "playback", &ss, NULL, NULL, &error))) {
        fprintf(stderr, __FILE__": pa_simple_new() failed: %s\n", pa_strerror(error));
        goto finish;
    }
    for (;;) {
        uint8_t buf[BUFSIZE];
        ssize_t r;
#if 0
        pa_usec_t latency;
        if ((latency = pa_simple_get_latency(s, &error)) == (pa_usec_t) -1) {
            fprintf(stderr, __FILE__": pa_simple_get_latency() failed: %s\n", pa_strerror(error));
            goto finish;
        }
        fprintf(stderr, "%0.0f usec    \r", (float)latency);
#endif
        /* Read some data ... */
        if ((r = read(STDsoundFileInfoNO, buf, sizeof(buf))) <= 0) {
            if (r == 0) /* EOF */
                break;
            fprintf(stderr, __FILE__": read() failed: %s\n", strerror(errno));
            goto finish;
        }
        /* ... and play it */
        if (pa_simple_write(s, buf, (size_t) r, &error) < 0) {
            fprintf(stderr, __FILE__": pa_simple_write() failed: %s\n", pa_strerror(error));
            goto finish;
        }
    }
    /* Make sure that every single sample was played */
    if (pa_simple_drain(s, &error) < 0) {
        fprintf(stderr, __FILE__": pa_simple_drain() failed: %s\n", pa_strerror(error));
        goto finish;
    }
    ret = 0;
finish:
    if (s)
        pa_simple_free(s);
    return ret;
}
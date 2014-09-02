#!/bin/sh
    echo "Content-type: text/html\n"

    # read in our parameters
    CMD=`echo "$QUERY_STRING" | sed -n 's/^.*cmd=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`
    FOLDER=`echo "$QUERY_STRING" | sed -n 's/^.*folder=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"| sed "s/%2F/\//g"`
    FOLDER1=`echo "$QUERY_STRING" | sed -n 's/^.*folder1=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"| sed "s/%2F/\//g"`
    TOTAL_REQUEST=`echo "$QUERY_STRING" | sed -n 's/^.*total_request=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"| sed "s/%2F/\//g"`
    CURRENT_CONNECTIONS=`echo "$QUERY_STRING" | sed -n 's/^.*current_connections=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"| sed "s/%2F/\//g"`
    ENDPOINT=`echo "$QUERY_STRING" | sed -n 's/^.*endpoint=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"| sed "s/%2F/\//g"`
    ITERATIONS=`echo "$QUERY_STRING" | sed -n 's/^.*iterations=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"| sed "s/%2F/\//g"`

    # our html header
    echo "<html>"
    echo "<head><title>ELB Client Test CGI</title></head>"
    echo "<body>"


    # page header
    echo "<p>"
    echo "<center>"
    echo "<h2>Bash commands</h2>"
    echo "</center>"
    echo "<p>"
    echo "<p>"

    echo "Choose which command you want to run"
    echo "<form method=get>"
    echo "<input type=radio name=cmd value=ifconfig checked> ifconfig (Network configuration) <br>"
    echo "<input type=radio name=cmd value=uname> uname -a (Kernel version)<br>"
    echo "<input type=radio name=cmd value=dmesg> dmesg (System messages) <br>"
    echo "<input type=radio name=cmd value=df> df -h (Free disk space) <br>"
    echo "<input type=radio name=cmd value=free> free (Memory info)<br>"
    echo "<input type=radio name=cmd value=cpuinfo> Cpu information <br>"
    echo "<input type=radio name=cmd value=hw> Hardware listing <br>"
    echo "<input type=radio name=cmd value=lsal> ls -al -- folder <input type=text name=folder1 value=/mnt/flash><br>"
    echo "<input type=radio name=cmd value=ab> ab
            -c <input type=text name=current_connections value=5>
            -n <input type=text name=total_request value=10>
            endpoint <input type=text name=endpoint value=127.0.0.1>
            FOR <input type=text name=iterations value=10> TIMES<br>"
    echo "<input type=submit>"
    echo "</form>"
    echo "</body>"


    # test if any parameters were passed

    if [ $CMD ]
    then
      case "$CMD" in
        ifconfig)
          echo "Output of ifconfig :<pre>"
          /sbin/ifconfig
          echo "</pre>"
          ;;

        uname)
          echo "Output of uname -a :<pre>"
          /bin/uname -a
          echo "</pre>"
          ;;

        dmesg)
          echo "Output of dmesg :<pre>"
          /bin/dmesg
          echo "</pre>"
          ;;

        df)
          echo "Output of df -h :<pre>"
          /bin/df -h
          echo "</pre>"
          ;;

        free)
          echo "Output of free :<pre>"
          /usr/bin/free
          echo "</pre>"
          ;;

         hw)
              echo "Hardware listing :<pre>"
              /usr/bin/lshw
              echo "</pre>"
              ;;

        lsal)
            echo "Output of ls $FOLDER1 :<pre>"
            /bin/ls -al "$FOLDER1"
            echo "</pre>"
            ;;


        cpuinfo)
              echo "Cpu information :<pre>"
              cat /proc/cpuinfo
              echo "</pre>"
              ;;
        
        ab)
            echo "Apache Benchmark $ITERATIONS times : ab -n $TOTAL_REQUEST -c $CURRENT_CONNECTIONS http://$ENDPOINT/<pre>"
            for i in $(seq 1 $ITERATIONS)
            do
                echo "$i ITERATION:"
                /usr/bin/ab -n $TOTAL_REQUEST -c $CURRENT_CONNECTIONS http://$ENDPOINT/
                echo "sleep 1"
                sleep 1
            done
            echo "</pre>"
            ;;
        *)
          echo "Unknown command $CMD<br>"
          ;;
      esac
    fi

    # print out the form
    echo "</html>"
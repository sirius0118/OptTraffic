import os
def gen_lua(app_name, compute_size, req_size, res_size, downstream):
    # app_name = sys.argv[1]
    # compute_size = sys.argv[2]
    # req_size = sys.argv[3]
    # res_size = sys.argv[4]
    # downstream = sys.argv[5]

    f = open('/home/k8s/exper/zxz/MSScheduler_python/DAG/build/serve.lua', 'r')
    g = open('/home/k8s/exper/zxz/MSScheduler_python/DAG/build/gen-lua/' + app_name + '.lua', 'w')

    text = f.readline()
    flag = 1
    while text:
        if flag:
            if 'compute_size' in text:
                text = 'compute_size = ' + str(compute_size) + '\n'
            if 'req_size' in text:
                text = 'req_size = ' + str(req_size) + '\n'
            if 'res_size' in text:
                text = 'res_size = ' + str(res_size) + '\n'
            if 'downstream' in text:
                if 'none' in text:
                    text = 'downstream = {}'
                else:
                    if isinstance(downstream, list):
                    # nums = downstream.split(',')
                        text = 'downstream = {'
                        for i in downstream[:-1]:
                            text = text + '\"' + i + '\",'
                        text = text + '\"' + downstream[-1] + '\"'
                        text = text + '}\n'
                    elif isinstance(downstream, str):
                        text = "downstream = {\""+ downstream + "\"}\n"
                flag = 0
        g.write(text)
        text = f.readline()

    g.close()
    f.close()

    os.system(f"scp /home/k8s/exper/zxz/MSScheduler_python/DAG/build/gen-lua/{app_name}.lua knode2:/tmp/{app_name}.lua &")
    os.system(f"scp /home/k8s/exper/zxz/MSScheduler_python/DAG/build/gen-lua/{app_name}.lua knode3:/tmp/{app_name}.lua &")
    os.system(f"scp /home/k8s/exper/zxz/MSScheduler_python/DAG/build/gen-lua/{app_name}.lua knode4:/tmp/{app_name}.lua &")
    os.system(f"scp /home/k8s/exper/zxz/MSScheduler_python/DAG/build/gen-lua/{app_name}.lua knode6:/tmp/{app_name}.lua &")
    os.system(f"scp /home/k8s/exper/zxz/MSScheduler_python/DAG/build/gen-lua/{app_name}.lua knode7:/tmp/{app_name}.lua &")
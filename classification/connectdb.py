# -*- coding: utf-8 -*-
if __name__ == "connectdb":
#if __name__ == "__main__":
    import sys
    sys.path.insert(0,"..\\cola")
    sys.path.insert(0,"D:\\09Limited_buffer\\earlywarningbyci\\classification\\trainmodel\\src")
    from contrib.weibo.storage import MicroBlog
    from cola.core.errors import DependencyNotInstalledError

    from contrib.weibo.conf import mongo_host, mongo_port, db_name, shard_key

    try:
        from mongoengine import connect, Document, EmbeddedDocument, \
                                DoesNotExist, Q, \
                                StringField, DateTimeField, EmailField, \
                                BooleanField, URLField, IntField, FloatField, \
                                ListField, EmbeddedDocumentField, \
                                ValidationError
    except ImportError:
        raise DependencyNotInstalledError('mongoengine')

    connect(db_name, host=mongo_host, port=mongo_port)

    DoesNotExist = DoesNotExist
    Q = Q
    ValidationError = ValidationError

    fout=open("before_predict.txt","wt")
    for i in MicroBlog.objects:
        print >>fout,i.mid.encode('utf-8'),"	".encode('utf-8'),\
              i.content.encode('utf-8'),"	".encode('utf-8'),\
              i.n_likes+i.n_forwards+i.n_comments,"	".encode('utf-8'),\
              i.created,"	".encode('utf-8'),\
              i.content.encode('utf-8')
    fout.close()

    import tms
#tms.tms_segment("before_predict.txt",out_filename="before_predict_seg.txt",\
#              seg=1,indexes=[1],str_splitTag=" ",)
    tms.tms_predict("before_predict.txt","D:\\09Limited_buffer\\earlywarningbyci\\classification\\trainmodel\\data\\model\\tms.config",\
                    result_save_path="predicted.txt",\
                    seg=1,str_splitTag=" ",\
                    indexes=[1],\
                    result_indexes=[0,2,3,4])
                    #result_indexes=[0,1,2])

    filterout=open("predicted.txt","r")
    afterfilter=open("filter.csv","wt")
    print >>afterfilter,"mid,focus,created,content"
    lines=filterout.readlines()
    for i in lines:
        list=i.split()
        label=list[0]
        mic_id=list[2]
        mic_focus=list[3]
        mic_created=list[4]+" "+list[5]
        list_length = len(list)
        mic_content=list[6]
        for k in range(7,list_length):
            mic_content=mic_content+list[k]
        if label=="-1.0":
            print >>afterfilter,mic_id,",",mic_focus,",",mic_created,",\"",mic_content,"\""
    filterout.close()
    afterfilter.close()

# Paper_Venue_Data_Mining_Analysis
- Advance Data Mining Course
- Dataset from DBLP

## Data Extractor 要求:
会议如下
EDBT
SDM
ICDE
CIKM
CVPR
VLDB
PODS
PAKDD
PKDD
ECML
AAAI
ECIR
SIGIR
WWW
IJCAI
SIGMOD Conference
ICDM
KDD
ICML
WSDM

需要的结果是：
Paper 对应的号码(已经有啦)
需要的文件:
Paper---对应的author  (paper1 author 1, paper 1  author 2)
Paper---对应的20个conferences/venues (如上列出)
Paper---对应的citation papers （编号data已经有了),有些没有列出是空的,就不要了。
Paper ----publish year

Raw data的格式说明:
#* --- paperTitle
#@ --- Authors
#t ---- Year
#c  --- publication venue
#index 00---- index id of this paper
#% ---- the id of references of this paper (there are multiple lines, with each indicating a reference)

你爬数据的时候就是删除前面的#， @，* 这些

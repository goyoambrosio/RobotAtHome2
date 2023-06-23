<div class="abstract" id="orgafb2a37">
<p>
Robot@Home is a dataset of raw data captured from the sensors of a mobile robot
in different indoor navigation sessions carried out in different homes. The
dataset is suitable for the development and testing of indoor mobile robotics
algorithms, especially in the field of semantic mapping. In this paper we
present Robot@Home2 Toolbox consisting of a Python package, a database and a set
of learning resources that comes to substitute original dataset for easy and
usable experimentation. The Python package contains database interface functions
and display functions, among others. The database forms the dataset itself
according to a relational model. In addition, the toolbox contains training
resources in the form of Jupyter notebooks. Robot@Home2 is open source and it is
available from the corresponding git repository or by installing it as a
standard Python package. The database can be easily downloaded programatically
or by accessing a public repository as Zenodo. In addition, the installation and
execution of Robot@Home2 is possible both in the local environment and in the
cloud.
</p>

</div>

# Appendix A. A survey on the previous use of Robot@Home dataset

| paper                                          | year | main topics                    | A      | B      | C      | D      | E      |
| <&ruiz-sarmiento2016_probabilistic_techniques> | 2016 | semantic mapping               |        |        |        |        | &bull; |
| <&ruiz-sarmiento2017_building_multiversal>     | 2017 | semantic mapping               |        |        |        |        | &bull; |
| <&nakamura2017_ensemble>                       | 2017 | object categorization, dataset |        |        | &bull; |        |        |
| <&ruiz-sarmiento2017_modelado_contexto>        | 2017 | semantic mapping               |        |        |        |        | &bull; |
| <&tarifa2017_motion>                           | 2017 | planar odometry                | &bull; |        |        |        |        |
| <&jaimez2017_motion_estimation>                | 2017 | planar odometry                | &bull; |        |        |        | &bull; |
| <&deeken2018_grounding>                        | 2018 | semantic mapping               |        |        |        | &bull; |        |
| <&jaimez2018_robust>                           | 2018 | plannar odometry               |        |        |        |        | &bull; |
| <&gunther2018_context>                         | 2018 | 3D world modelling             |        |        |        | &bull; |        |
| <&roa-borbolla2018_realistic>                  | 2018 | map generation, simulation     |        |        |        | &bull; |        |
| <&ferri2018_computing_fast>                    | 2018 | motion planning                | &bull; |        | &bull; |        |        |
| <&suh2018_semantic_task>                       | 2018 | task planning                  |        |        |        | &bull; |        |
| <&balloch2018_unbiasing>                       | 2018 | semantic segmentation          |        |        |        | &bull; | &bull; |
| <&pire2019_rosario>                            | 2019 | SLAM, dataset                  |        |        |        | &bull; |        |
| <&ruiz-sarmiento2019_ontology>                 | 2019 | object recognition             |        |        |        |        | &bull; |
| <&zuniga2019_automatic>                        | 2019 | sensor calibration             |        |        | &bull; |        |        |
| <&chaves2019_integration>                      | 2019 | semantic mapping               |        |        |        |        | &bull; |
| <&martinez2019_fukuoka>                        | 2019 | dataset                        |        |        |        | &bull; |        |
| <&delapuente2019_robot>                        | 2019 | indoor navigation              |        |        |        | &bull; |        |
| <&mishra2019_ego>                              | 2019 | robotic hardware               |        |        | &bull; |        |        |
| <&zuniga-noel2019_intrinsic>                   | 2019 | sensor calibration             |        |        | &bull; |        |        |
| <&monroy2019_olfaction_vision>                 | 2019 | robotic olfaction, obj. rec.   |        |        |        |        | &bull; |
| <&ruiz-sarmiento2019_tutorial_on>              | 2019 | training                       |        |        |        |        | &bull; |
| <&fabro2019_design_development>                | 2019 | dataset                        |        |        | &bull; |        |        |
| <&baltanas2019_coleccion_jupyter>              | 2019 | training                       |        |        | &bull; |        |        |
| <&moreno2020_automatic>                        | 2020 | path planning                  |        |        |        |        | &bull; |
| <&chen2020_advanced>                           | 2020 | dataset                        |        | &bull; |        | &bull; |        |
| <&fernandez-chaves2020_from_object>            | 2020 | reasoning, categorization      |        |        |        |        | &bull; |
| <&qi2020_object_lidar>                         | 2020 | semantic mapping               |        |        |        |        | &bull; |
| <&andersone2020_quality_evaluation>            | 2020 | map merging                    |        |        |        |        | &bull; |
| <&li2020_relative_pose>                        | 2020 | pose estimation                |        |        |        |        | &bull; |
| <&ruiz-sarmiento2020_tutorial_python>          | 2020 | training                       |        |        |        |        | &bull; |
| <&maffei2020_global_localization>              | 2020 | localization, path planning    |        |        |        |        | &bull; |
| <&garg2020_semantics_robotic>                  | 2020 | semantic mapping, survey       |        | &bull; |        | &bull; |        |
| <&roa-borbolla2020_algorithm_comparison>       | 2020 | path planning                  |        |        |        | &bull; |        |
| <&othman2020_towards>                          | 2020 | indoor navigation              | &bull; |        |        | &bull; |        |
| <&burgueno2020_collection_of>                  | 2020 | training                       |        |        |        | &bull; |        |
| <&pierre2020_localisation>                     | 2020 | localization                   | &bull; |        | &bull; |        |        |
| <&shu2021_slam_field>                          | 2021 | SLAM                           |        |        | &bull; |        |        |
| <&yu2021_drsnet>                               | 2021 | categorization                 |        |        | &bull; |        |        |
| <&fernandez-chaves2021_vimantic>               | 2021 | semantic mapping               |        |        |        |        | &bull; |
| <&burgueno-romero2021_autonomous>              | 2021 | path planning, learning        |        |        | &bull; |        |        |
| <&suveges2021_egomap>                          | 2021 | SLAM, dataset                  |        |        | &bull; |        |        |
| <&li2021_belief_space>                         | 2021 | navigation, uncertainty        | &bull; |        |        |        |        |
| <&asmanis2021_combining_semantics>             | 2021 | SLAM                           | &bull; |        | &bull; |        |        |
| <&qu2021_outline_multi>                        | 2021 | SLAM, sensor fusion            |        |        |        |        | &bull; |
| <&salhi2021_intelligent_embedded>              | 2021 | SLAM                           | &bull; |        | &bull; |        |        |
| <&jin2021_semantic_mapping>                    | 2021 | semantic mapping               |        |        |        |        | &bull; |
| <&chamzas2021_motionbenchmaker>                | 2021 | dataset                        |        | &bull; | &bull; |        |        |
| <&ruiz-sarmiento2021_jupyter_notebooks>        | 2021 | training                       |        |        | &bull; |        |        |
| <&luperto2021_exploration_indoor>              | 2021 | navigation, uncertainty        |        |        |        |        | &bull; |
| <&matez-bandera2021_efficient>                 | 2021 | categorization                 |        |        |        |        | &bull; |
| <&setiono2021_novel_room>                      | 2021 | categorization                 |        |        |        |        | &bull; |
| <&ge2021_capacitive_piezoresistive>            | 2021 | sensor hardware                |        |        | &bull; |        |        |
| <&liu2021_simultaneous_localization>           | 2021 | SLAM, dataset, survey          |        | &bull; | &bull; |        |        |
| <&liu2021_datasets_evaluation>                 | 2021 | SLAM, dataset, survey          |        | &bull; | &bull; |        |        |

Since its publication, Robot@Home dataset <&ruiz-sarmiento2017_robotic_dataset> has been referenced in a significant number of papers. We have carried out a survey (Table [1](#org5eaac27)) to understand how the community has been using the dataset and the challenges they have faced using it.

On some occasions the dataset was referenced as an example of the importance of datasets in the area of mobile robotics <&nakamura2017_ensemble;&zuniga2019_automatic;&mishra2019_ego;&zuniga-noel2019_intrinsic;&fabro2019_design_development;&shu2021_slam_field;&yu2021_drsnet;&burgueno-romero2021_autonomous;&suveges2021_egomap;&chamzas2021_motionbenchmaker;&ge2021_capacitive_piezoresistive;&liu2021_simultaneous_localization;&liu2021_datasets_evaluation>, and on other occasions more specifically as a dataset oriented to semantic mapping <&deeken2018_grounding;&gunther2018_context;&roa-borbolla2018_realistic;&suh2018_semantic_task;&pire2019_rosario;&martinez2019_fukuoka;&delapuente2019_robot;&garg2020_semantics_robotic;&roa-borbolla2020_algorithm_comparison;&burgueno2020_collection_of>. It has also served as a source of inspiration for PhD thesis <&ruiz-sarmiento2016_probabilistic_techniques;&tarifa2017_motion;&jaimez2017_motion_estimation;&ferri2018_computing_fast;&othman2020_towards;&pierre2020_localisation;&li2021_belief_space;&asmanis2021_combining_semantics;&salhi2021_intelligent_embedded> and as an education resource <&ruiz-sarmiento2021_jupyter_notebooks;&ruiz-sarmiento2019_tutorial_on;&ruiz-sarmiento2020_tutorial_python>

However, where the data set has been most useful and of greatest interest to us has been in those works in which it has been used for the purpose for which it was created, that is, as a testing platform for the development of algorithms.

Robot@Home dataset has been exploited for a variety of tasks. Starting with semantic mapping, in <&ruiz-sarmiento2017_building_multiversal;&monroy2019_olfaction_vision> Robot@Home dataset was used to check the suitability of a probabilistic representation in form of semantic map and its capacity to handle uncertain information. This map is an extension of traditional semantic maps for robotics, with the ability to coherently manage uncertain information coming from, for example, object recognition or gas classification processes, and reference them to the location where they were acquired into a metric map. Additionally, it also comprises semantic information codified by means of an ontology, enabling the execution of high-level reasoning tasks. <&chaves2019_integration> proposes the integration of a cnn into a robotic architecture to build semantic maps of indoor environments and carries out experiments with Robot@Home dataset. On the other hand, <&fernandez-chaves2021_vimantic> presents ViMantic as a novel semantic mapping architecture for the building and maintenance of such maps. Experiments were carried out with the Robot@Home dataset considering multiple robots collecting data from the same environment, hence enabling the testing of multi-agent scenarios. In <&jin2021_semantic_mapping> a new deep learning-based image feature fusion method is presented. The RGB feature information extracted by a classification network and a detection network are integrated to improve the robot’s scene recognition ability and make the acquired semantic information more accurate. Robot@Home dataset is used to test a 2d metric map obtained with the proposed the method.

Other works related to room categorization have made use of the dataset. In <&fernandez-chaves2020_from_object> proposes a room categorization system based on a Bayesian probabilistic framework that combines object detections and its semantics. The proposed system is evaluated in houses from the Robot@Home dataset, validating its effectiveness under real-world conditions. Moreover, <&setiono2021_novel_room> implements room categorization via scene understanding by integrating available object information in the scene, proposing a novel approach based on the prior knowledge of the object appearance frequency in the specific room category inside the house. The proposed approach is tested and evaluated by applying the Robot@Home dataset using the available RGB images under specific room categories.

In <&tarifa2017_motion;&jaimez2018_robust> simulations using Robot@Home and other datasets are carried out to address the estimation of 2D and 3D motion with different kinds of range sensors. Otherwise, ontology-based conditional random fields address the problem of object recognition <&ruiz-sarmiento2019_ontology> using again scenes from Robot@Home to test the approach. <&moreno2020_automatic> introduces an automatic waypoint generation method to improve robot navigation through narrow spaces. This work mainly uses Robot@Home dataset and justifies it due to the lack of publicly available databases that contain occupancy grids of real houses, being usually focused on labs and offices instead. <&balloch2018_unbiasing> proposes improving the performance of real-time segmentation frameworks on robot perception data by transferring features learned from synthetic segmentation data. Their work takes advantage of Robot@Home by fine-tuning on various subsets of the dataset to quantify the benefits as the amount of supervised fine-tuning data is decreased. Moreover <&luperto2020_exploration;&luperto2021_exploration_indoor> present an approach to map building that exploits a prediction of the geometric structure of the unknown parts of an environment to improve exploration performance applying it to partial grid maps acquired in real environments. An example of a computed map obtained by a real robot is created from the Robot@Home dataset.

In <&qi2020_object_lidar> an object semantic grid mapping system with 2D LiDAR and RGB-D sensors is proposed to solve the lack of semantic information to endow the robots with the ability of social goal selection and human-friendly operation modes. To verify the the effectiveness of the system the Robot@Home dataset is used again. On the other hand <&andersone2020_quality_evaluation> proposes a method that allows the quality evaluation of occupancy grid maps without the need for ground truth maps. The method uses Convolutional Neural Network (CNN) for map fragment classification, for map quality evaluation as well as for evaluation of map regions. To train and test the CNN, data of various quality maps was collected from several open source data sets including Robot@Home.

Furthermore, <&li2020_relative_pose> presents a complete comprehensive study of the relative pose estimation problem for a calibrated camera constrained by known SE(3) invariant. To compare some approaches RGBD images from front and left cameras of Robot@Home are used. <&maffei2020_global_localization> presents a localization strategy using floor plan as map, which is based on spatial density information computed from dense depth data of RGB-D cameras. The experimental validation is made using the Robot@home dataset. As the ground truth of the robot pose and the odometry are not directly available, they are respectively generated using SLAM and scan matching techniques. For each scenario, two types of tests were performed: multi-camera by using the four RGB-D cameras, and single-camera by using only the RGB-D camera facing forward. And <&matez-bandera2021_efficient> presents an attention mechanism for mobile robots to face the problem of place categorization. Robot@Home is used to demostrate that the proposal generalizes well for the two main paradigms of place categorization (object-based and image-based), outperforming typical camera-configurations (fixed and continuously-rotating) and a pure-exploratory approach, both in quickness and accuracy. As Robot@Home does not explicitly offer a controllable pan unit a virtual one with degrees of pan motion and a maximum rotation speed of degrees per second is generated by interpolating the view from the four available fixed cameras.

<PhD.bib>

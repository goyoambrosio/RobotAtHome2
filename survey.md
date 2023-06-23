
# A survey on the previous use of Robot@Home dataset


Since its publication, Robot@Home dataset
(Ruiz-Sarmiento, Galindo, and González-Jiménez 2017) has been referenced in a significant
number of papers. We have carried out a survey ([Table 1](#org34921bc)) to understand how the community
has been using the dataset and the challenges they have faced using it.

On some occasions the dataset was referenced as an example of the importance of datasets
in the area of mobile robotics
(Nakamura and Nagai 2017; Zuñiga-Noël et al. 2019; Mishra et al. 2019; Zuñiga-Noël, Ruiz-Sarmiento, and Gonzalez-Jimenez 2019; Fabro, Vaz, and Oliveira 2019; Shu et al. 2021; Yu and Fan 2021; Burgueño-Romero, Ruiz-Sarmiento, and Gonzalez-Jimenez 2021; Suveges and McKenna 2021; Chamzas et al. 2021; Ge et al. 2021; Liu et al. 2021b, 2021a),
and on other occasions more specifically as a dataset oriented to semantic
mapping
(Deeken, Wiemann, and Hertzberg 2018; Günther et al. 2018; Roa-Borbolla et al. 2018; Suh 2018; Pire et al. 2019; Martinez Mozos et al. 2019; De La Puente et al. 2019; Garg et al. 2020; Roa-Borbolla et al. 2020; Burgueño Romero et al. 2020).
It has also served as a source of inspiration for PhD thesis
(Ruiz-Sarmiento 2016; Tarifa and others 2017; Jaimez Tarifa and others 2017; Ferri 2018; Othman 2020; Pierre 2020; Li 2021; Asmanis 2021; Salhi 2021)
and as an education resource (Ruiz-Sarmiento, Baltanas, and Gonzalez-Jimenez 2021; Ruiz-Sarmiento, Monroy, et al. 2019; Ruiz-Sarmiento et al. 2020)

However, where the data set has been most useful and of greatest interest to us
has been in those works in which it has been used for the purpose for which it
was created, that is, as a testing platform for the development of algorithms.

Robot@Home dataset has been exploited for a variety of tasks. Starting with
semantic mapping, in
(Ruiz-Sarmiento, Galindo, and Gonzalez-Jimenez 2017; Monroy et al. 2019)
Robot@Home dataset was used to check the suitability of a probabilistic
representation in form of semantic map and its capacity to handle uncertain
information. This map is an extension of traditional semantic maps for robotics,
with the ability to coherently manage uncertain information coming from, for
example, object recognition or gas classification processes, and reference them
to the location where they were acquired into a metric map. Additionally, it
also comprises semantic information codified by means of an ontology, enabling
the execution of high-level reasoning tasks. (Chaves et al. 2019)
proposes the integration of a cnn into a robotic architecture to build semantic
maps of indoor environments and carries out experiments with Robot@Home dataset.
On the other hand, (Fernandez-Chaves et al. 2021) presents ViMantic as a
novel semantic mapping architecture for the building and maintenance of such
maps. Experiments were carried out with the Robot@Home dataset considering
multiple robots collecting data from the same environment, hence enabling the
testing of multi-agent scenarios. In (Jin et al. 2021) a new deep
learning-based image feature fusion method is presented. The RGB feature
information extracted by a classification network and a detection network are
integrated to improve the robot’s scene recognition ability and make the
acquired semantic information more accurate. Robot@Home dataset is used to test
a 2d metric map obtained with the proposed the method.

Other works related to room categorization have made use of the dataset. In
(Fernandez-Chaves et al. 2020) proposes a room categorization system
based on a Bayesian probabilistic framework that combines object detections and
its semantics. The proposed system is evaluated in houses from the Robot@Home
dataset, validating its effectiveness under real-world conditions. Moreover,
(Setiono, Elibol, and Chong 2021) implements room categorization via scene
understanding by integrating available object information in the scene, proposing
a novel approach based on the prior knowledge of the object appearance frequency
in the specific room category inside the house. The proposed approach is tested
and evaluated by applying the Robot@Home dataset using the available RGB images
under specific room categories.

In (Tarifa and others 2017; Jaimez et al. 2018) simulations using Robot@Home and
other datasets are carried out to address the estimation of 2D and 3D motion
with different kinds of range sensors. Otherwise, ontology-based conditional
random fields address the problem of object recognition
(Ruiz-Sarmiento, Galindo, et al. 2019) using again scenes from Robot@Home to test the
approach. (Moreno et al. 2020) introduces an automatic waypoint generation
method to improve robot navigation through narrow spaces. This work mainly uses
Robot@Home dataset and justifies it due to the lack of publicly available
databases that contain occupancy grids of real houses, being usually focused on
labs and offices instead. (Balloch et al. 2018) proposes improving the
performance of real-time segmentation frameworks on robot perception data by
transferring features learned from synthetic segmentation data. Their work takes
advantage of Robot@Home by fine-tuning on various subsets of the dataset to
quantify the benefits as the amount of supervised fine-tuning data is decreased.
Moreover (Luperto, Fochetta, and Amigoni 2020, 2021) present
an approach to map building that exploits a prediction of the geometric
structure of the unknown parts of an environment to improve exploration
performance applying it to partial grid maps acquired in real environments. An
example of a computed map obtained by a real robot is created from the
Robot@Home dataset.

In (Qi et al. 2020) an object semantic grid mapping system with 2D
LiDAR and RGB-D sensors is proposed to solve the lack of semantic information to
endow the robots with the ability of social goal selection and human-friendly
operation modes. To verify the the effectiveness of the system the Robot@Home
dataset is used again. On the other hand (Andersone 2020)
proposes a method that allows the quality evaluation of occupancy grid maps
without the need for ground truth maps. The method uses Convolutional Neural
Network (CNN) for map fragment classification, for map quality evaluation as
well as for evaluation of map regions. To train and test the CNN, data of
various quality maps was collected from several open source data sets including
Robot@Home.

Furthermore, (Li, Martyushev, and Lee 2020) presents a complete comprehensive study
of the relative pose estimation problem for a calibrated camera constrained by
known SE(3) invariant. To compare some approaches RGBD images from front and
left cameras of Robot@Home are used. (Maffei et al. 2020)
presents a localization strategy using floor plan as map, which is based on
spatial density information computed from dense depth data of RGB-D cameras. The
experimental validation is made using the Robot@home dataset. As the ground
truth of the robot pose and the odometry are not directly available, they are
respectively generated using SLAM and scan matching techniques. For each
scenario, two types of tests were performed: multi-camera by using the four
RGB-D cameras, and single-camera by using only the RGB-D camera facing forward.
And (Matez-Bandera, Monroy, and Gonzalez-Jimenez 2021) presents an attention mechanism for mobile
robots to face the problem of place categorization. Robot@Home is used to
demostrate that the proposal generalizes well for the two main paradigms of
place categorization (object-based and image-based), outperforming typical
camera-configurations (fixed and continuously-rotating) and a pure-exploratory
approach, both in quickness and accuracy. As Robot@Home does not explicitly
offer a controllable pan unit a virtual one with degrees of pan motion and a
maximum rotation speed of degrees per second is generated by interpolating the
view from the four available fixed cameras.

<table id="org34921bc" border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">
<caption class="t-above"><span class="table-number">Table 1:</span> Works that have used or featured Robot@Home in some way. (A) This work is a <b>PhD thesis</b> dissertation. The dataset has been used or taken into account for the work. (B) This work is a <b>survey</b> that refers the dataset. (C) This work refers the dataset as an example of its importance in the field of <b>mobile robotics</b>. (D) This work refers the dataset in the field of <b>semantic mapping</b>. (E) In this work Robot@Home has contributed <b>in depth</b> in its verification.</caption>

<colgroup>
<col  class="org-left" />

<col  class="org-right" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">paper</th>
<th scope="col" class="org-right">year</th>
<th scope="col" class="org-left">main topics</th>
<th scope="col" class="org-left">A</th>
<th scope="col" class="org-left">B</th>
<th scope="col" class="org-left">C</th>
<th scope="col" class="org-left">D</th>
<th scope="col" class="org-left">E</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">(Ruiz-Sarmiento 2016)</td>
<td class="org-right">2016</td>
<td class="org-left">semantic mapping</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
</tr>


<tr>
<td class="org-left">(Ruiz-Sarmiento, Galindo, and Gonzalez-Jimenez 2017)</td>
<td class="org-right">2017</td>
<td class="org-left">semantic mapping</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
</tr>


<tr>
<td class="org-left">(Nakamura and Nagai 2017)</td>
<td class="org-right">2017</td>
<td class="org-left">object categorization, dataset</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">(Jose-Raul Ruiz-Sarmiento 2017)</td>
<td class="org-right">2017</td>
<td class="org-left">semantic mapping</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
</tr>


<tr>
<td class="org-left">(Tarifa and others 2017)</td>
<td class="org-right">2017</td>
<td class="org-left">planar odometry</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">(Jaimez Tarifa and others 2017)</td>
<td class="org-right">2017</td>
<td class="org-left">planar odometry</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
</tr>


<tr>
<td class="org-left">(Deeken, Wiemann, and Hertzberg 2018)</td>
<td class="org-right">2018</td>
<td class="org-left">semantic mapping</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">(Jaimez et al. 2018)</td>
<td class="org-right">2018</td>
<td class="org-left">plannar odometry</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
</tr>


<tr>
<td class="org-left">(Günther et al. 2018)</td>
<td class="org-right">2018</td>
<td class="org-left">3D world modelling</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">(Roa-Borbolla et al. 2018)</td>
<td class="org-right">2018</td>
<td class="org-left">map generation, simulation</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">(Ferri 2018)</td>
<td class="org-right">2018</td>
<td class="org-left">motion planning</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">(Suh 2018)</td>
<td class="org-right">2018</td>
<td class="org-left">task planning</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">(Balloch et al. 2018)</td>
<td class="org-right">2018</td>
<td class="org-left">semantic segmentation</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&bull;</td>
</tr>


<tr>
<td class="org-left">(Pire et al. 2019)</td>
<td class="org-right">2019</td>
<td class="org-left">SLAM, dataset</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">(Ruiz-Sarmiento, Galindo, et al. 2019)</td>
<td class="org-right">2019</td>
<td class="org-left">object recognition</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
</tr>


<tr>
<td class="org-left">(Zuñiga-Noël et al. 2019)</td>
<td class="org-right">2019</td>
<td class="org-left">sensor calibration</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">(Chaves et al. 2019)</td>
<td class="org-right">2019</td>
<td class="org-left">semantic mapping</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
</tr>


<tr>
<td class="org-left">(Martinez Mozos et al. 2019)</td>
<td class="org-right">2019</td>
<td class="org-left">dataset</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">(De La Puente et al. 2019)</td>
<td class="org-right">2019</td>
<td class="org-left">indoor navigation</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">(Mishra et al. 2019)</td>
<td class="org-right">2019</td>
<td class="org-left">robotic hardware</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">(Zuñiga-Noël, Ruiz-Sarmiento, and Gonzalez-Jimenez 2019)</td>
<td class="org-right">2019</td>
<td class="org-left">sensor calibration</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">(Monroy et al. 2019)</td>
<td class="org-right">2019</td>
<td class="org-left">robotic olfaction, obj. rec.</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
</tr>


<tr>
<td class="org-left">(Ruiz-Sarmiento, Monroy, et al. 2019)</td>
<td class="org-right">2019</td>
<td class="org-left">training</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
</tr>


<tr>
<td class="org-left">(Fabro, Vaz, and Oliveira 2019)</td>
<td class="org-right">2019</td>
<td class="org-left">dataset</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">(Baltanas Molero, Ruiz Sarmiento, and Gonzalez-Jimenez 2019)</td>
<td class="org-right">2019</td>
<td class="org-left">training</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">(Moreno et al. 2020)</td>
<td class="org-right">2020</td>
<td class="org-left">path planning</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
</tr>


<tr>
<td class="org-left">(Chen et al. 2020)</td>
<td class="org-right">2020</td>
<td class="org-left">dataset</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">(Fernandez-Chaves et al. 2020)</td>
<td class="org-right">2020</td>
<td class="org-left">reasoning, categorization</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
</tr>


<tr>
<td class="org-left">(Qi et al. 2020)</td>
<td class="org-right">2020</td>
<td class="org-left">semantic mapping</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
</tr>


<tr>
<td class="org-left">(Andersone 2020)</td>
<td class="org-right">2020</td>
<td class="org-left">map merging</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
</tr>


<tr>
<td class="org-left">(Li, Martyushev, and Lee 2020)</td>
<td class="org-right">2020</td>
<td class="org-left">pose estimation</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
</tr>


<tr>
<td class="org-left">(Ruiz-Sarmiento et al. 2020)</td>
<td class="org-right">2020</td>
<td class="org-left">training</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
</tr>


<tr>
<td class="org-left">(Maffei et al. 2020)</td>
<td class="org-right">2020</td>
<td class="org-left">localization, path planning</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
</tr>


<tr>
<td class="org-left">(Garg et al. 2020)</td>
<td class="org-right">2020</td>
<td class="org-left">semantic mapping, survey</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">(Roa-Borbolla et al. 2020)</td>
<td class="org-right">2020</td>
<td class="org-left">path planning</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">(Othman 2020)</td>
<td class="org-right">2020</td>
<td class="org-left">indoor navigation</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">(Burgueño Romero et al. 2020)</td>
<td class="org-right">2020</td>
<td class="org-left">training</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">(Pierre 2020)</td>
<td class="org-right">2020</td>
<td class="org-left">localization</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">(Shu et al. 2021)</td>
<td class="org-right">2021</td>
<td class="org-left">SLAM</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">(Yu and Fan 2021)</td>
<td class="org-right">2021</td>
<td class="org-left">categorization</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">(Fernandez-Chaves et al. 2021)</td>
<td class="org-right">2021</td>
<td class="org-left">semantic mapping</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
</tr>


<tr>
<td class="org-left">(Burgueño-Romero, Ruiz-Sarmiento, and Gonzalez-Jimenez 2021)</td>
<td class="org-right">2021</td>
<td class="org-left">path planning, learning</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">(Suveges and McKenna 2021)</td>
<td class="org-right">2021</td>
<td class="org-left">SLAM, dataset</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">(Li 2021)</td>
<td class="org-right">2021</td>
<td class="org-left">navigation, uncertainty</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">(Asmanis 2021)</td>
<td class="org-right">2021</td>
<td class="org-left">SLAM</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">(Qu et al. 2021)</td>
<td class="org-right">2021</td>
<td class="org-left">SLAM, sensor fusion</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
</tr>


<tr>
<td class="org-left">(Salhi 2021)</td>
<td class="org-right">2021</td>
<td class="org-left">SLAM</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">(Jin et al. 2021)</td>
<td class="org-right">2021</td>
<td class="org-left">semantic mapping</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
</tr>


<tr>
<td class="org-left">(Chamzas et al. 2021)</td>
<td class="org-right">2021</td>
<td class="org-left">dataset</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">(Ruiz-Sarmiento, Baltanas, and Gonzalez-Jimenez 2021)</td>
<td class="org-right">2021</td>
<td class="org-left">training</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">(Luperto, Fochetta, and Amigoni 2021)</td>
<td class="org-right">2021</td>
<td class="org-left">navigation, uncertainty</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
</tr>


<tr>
<td class="org-left">(Matez-Bandera, Monroy, and Gonzalez-Jimenez 2021)</td>
<td class="org-right">2021</td>
<td class="org-left">categorization</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
</tr>


<tr>
<td class="org-left">(Setiono, Elibol, and Chong 2021)</td>
<td class="org-right">2021</td>
<td class="org-left">categorization</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
</tr>


<tr>
<td class="org-left">(Ge et al. 2021)</td>
<td class="org-right">2021</td>
<td class="org-left">sensor hardware</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">(Liu et al. 2021b)</td>
<td class="org-right">2021</td>
<td class="org-left">SLAM, dataset, survey</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>


<tr>
<td class="org-left">(Liu et al. 2021a)</td>
<td class="org-right">2021</td>
<td class="org-left">SLAM, dataset, survey</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&bull;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>
</tbody>
</table>

## Bibliography

Andersone, Ilze. 2020. “Quality Evaluation of the Occupancy Grids without Ground Truth Maps.” In ICAART (1), 319–26.

Asmanis, Ioannis. 2021. “Combining Semantics with Unified Geometric Representations for Indoor Slam.” National technical university of athens school of electrical and computer engineering.

Balloch, Jonathan C, Varun Agrawal, Irfan Essa, and Sonia Chernova. 2018. “Unbiasing Semantic Segmentation for Robot Perception Using Synthetic Data Feature Transfer.” arXiv Preprint arXiv:1809.03676.

Baltanas Molero, Samuel Felipe, José Raúl Ruiz Sarmiento, and Javier Gonzalez-Jimenez. 2019. “Colección de Jupyter Notebooks Para Cursos de Robótica Móvil.” In XL Jornadas de Automática, 663–70.

Burgueño-Romero, AM, JR Ruiz-Sarmiento, and Javier Gonzalez-Jimenez. 2021. “Autonomous Docking of Mobile Robots by Reinforcement Learning Tackling the Sparse Reward Problem.” In International Work-Conference on Artificial Neural Networks, 392–403. Springer.

Burgueño Romero, A.M., J.R. Ruiz Sarmiento, F.A. Moreno Dueñas, and J. Gonzalez Jimenez. 2020. “A Collection of Jupyter Notebooks Covering the Fundamentals of Computer Vision.” In ICERI2020 Proceedings, 5495–5505. 13th Annual International Conference of Education, Research and Innovation. Online Conference: IATED. <10.21125/iceri.2020.1189>.

Chamzas, Constantinos, Carlos Quintero-Pena, Zachary Kingston, Andreas Orthey, Daniel Rakita, Michael Gleicher, Marc Toussaint, and Lydia E Kavraki. 2021. “MOTIONBENCHMAKER: A Tool to Generate and Benchmark Motion Planning Datasets.” IEEE Robotics and Automation Letters 7 (2). IEEE: 882–89.

Chaves, D, JR Ruiz-Sarmiento, Nicolai Petkov, and J Gonzalez-Jimenez. 2019. “Integration of Cnn into a Robotic Architecture to Build Semantic Maps of Indoor Environments.” In International Work-Conference on Artificial Neural Networks, 313–24. Springer.

Chen, Hongyu, Zhijie Yang, Xiting Zhao, Guangyuan Weng, Haochuan Wan, Jianwen Luo, Xiaoya Ye, et al. 2020. “Advanced Mapping Robot and High-Resolution Dataset.” Robotics and Autonomous Systems 131. Elsevier: 103559.

Deeken, Henning, Thomas Wiemann, and Joachim Hertzberg. 2018. “Grounding Semantic Maps in Spatial Databases.” Robotics and Autonomous Systems 105. Elsevier: 146–65.

De La Puente, Paloma, Markus Bajones, Christian Reuther, Daniel Wolf, David Fischinger, and Markus Vincze. 2019. “Robot Navigation in Domestic Environments: Experiences Using RGB-D Sensors in Real Homes.” Journal of Intelligent & Robotic Systems 94 (2). Springer: 455–70.

Fabro, João, Marlon Vaz, and Andre Oliveira. 2019. “Design and Development of an Automated System for Creation of Image Datasets Intended to Allow Object Identification and Grasping by Service Robots.” In Anais Do 14 Congresso Brasileiro de Inteligência Computacional - CBIC2019, edited by Bruno José Torres Fernandes and Antônio Júnior\\, 1–6. Curitiba, PR: ABRICOM. <10.21528/CBIC2019-136>.

Fernandez-Chaves, David, Jose-Raul Ruiz-Sarmiento, Nicolai Petkov, and Javier Gonzalez-Jimenez. 2020. “From Object Detection to Room Categorization in Robotics.” In Proceedings of the 3rd International Conference on Applications of Intelligent Systems. APPIS 2020. Las Palmas de Gran Canaria, Spain: Association for Computing Machinery. <10.1145/3378184.3378230>.

Fernandez-Chaves, D, JR Ruiz-Sarmiento, N Petkov, and J Gonzalez-Jimenez. 2021. “ViMantic, a Distributed Robotic Architecture for Semantic Mapping in Indoor Environments.” Knowledge-Based Systems 232. Elsevier: 107440.

Ferri, Federico. 2018. “Computing Fast Search Heuristics for Physics-Based Mobile Robot Motion Planning.” Sapienza, University of Rome.

Garg, Sourav, Niko Sünderhauf, Feras Dayoub, Douglas Morrison, Akansel Cosgun, Gustavo Carneiro, Qi Wu, et al. 2020. “Semantics for Robotic Mapping, Perception and Interaction: A Survey.” Foundations and Trends® in Robotics 8 (1–2). Now Publishers: 1–224. <10.1561/2300000059>.

Ge, Chuanyang, Zhenlong Wang, Zhe Liu, Tianhao Wu, Shuai Wang, Xuanyu Ren, Diansheng Chen, Jie Zhao, PingAn Hu, and Jia Zhang. 2021. “A Capacitive and Piezoresistive Hybrid Sensor for Long-Distance Proximity and Wide-Range Force Detection in Human–Robot Collaboration.” Advanced Intelligent Systems. Wiley Online Library, 2100213.

Günther, M., J. R. Ruiz-Sarmiento, C. Galindo, J. Gonzalez-Jimenez, and J. Hertzberg. 2018. “Context-Aware 3d Object Anchoring for Mobile Robots.” Robotics and Autonomous Systems.

Jaimez, Mariano, Javier Monroy, Manuel Lopez-Antequera, and Javier Gonzalez-Jimenez. 2018. “Robust Planar Odometry Based on Symmetric Range Flow and Multiscan Alignment.” IEEE Transactions on Robotics 34 (6). IEEE: 1623–35.

Jaimez Tarifa, Mariano, and others. 2017. “Motion Estimation, 3D Reconstruction and Navigation with Range Sensors.” University of Málaga; UMA Editorial.

Jin, Cong, Armagan Elibol, Pengfei Zhu, and Nak Young Chong. 2021. “Semantic Mapping Based on Image Feature Fusion in Indoor Environments.” In 2021 21st International Conference on Control, Automation and Systems (ICCAS), 693–98. IEEE.

Jose-Raul Ruiz-Sarmiento, Javier Gonzalez-Jimenez Cipriano Galindo. 2017. “Modelado Del Contexto Geometrico Para El Reconocimiento de Objetos.” In Actas de Las XXXVIII Jornadas de Automática. Servicio de Publicaciones de la Universidad de Oviedo. <http://mapir.uma.es/papersrepo/2017/2017-raul-JA-Modelado_del_Contexto_Geometrico.pdf>.

Li, Binbin. 2021. “Belief Space-Guided Navigation for Robots and Autonomous Vehicles.” Texas A&M University.

Li, Bo, Evgeniy Martyushev, and Gim Hee Lee. 2020. “Relative Pose Estimation of Calibrated Cameras with Known SE(3) Invariant.” In European Conference on Computer Vision, 215–31. Springer.

Liu, Yuanzhi, Yujia Fu, Fengdong Chen, Bart Goossens, Wei Tao, and Hui Zhao. 2021a. “Datasets and Evaluation for Simultaneous Localization and Mapping Related Problems: A Comprehensive Survey.” arXiv E-Prints, arXiv–2102.

Liu, Yuanzhi and Fu, Yujia and Chen, Fengdong and Goossens, Bart and Tao, Wei and Zhao, Hui. 2021b. “Simultaneous Localization and Mapping Related Datasets: A Comprehensive Survey.” arXiv Preprint arXiv:2102.04036.

Luperto, Matteo, Luca Fochetta, and Francesco Amigoni. 2020. “Exploration of Indoor Environments Predicting the Layout of Partially Observed Rooms.” arXiv Preprint arXiv:2004.06967.

Luperto, Matteo and Fochetta, Luca and Amigoni, Francesco. 2021. “Exploration of Indoor Environments through Predicting the Layout of Partially Observed Rooms.” In Proceedings of the 20th International Conference on Autonomous Agents and MultiAgent Systems, 836–43.

Maffei, Renan, Diego Pittol, Mathias Mantelli, Edson Prestes, and Mariana Kolberg. 2020. “Global Localization over 2D Floor Plans with Free-Space Density Based on Depth Information.” In 2020 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 4609–14. IEEE.

Martinez Mozos, Oscar, Kazuto Nakashima, Hojung Jung, Yumi Iwashita, and Ryo Kurazume. 2019. “Fukuoka Datasets for Place Categorization.” The International Journal of Robotics Research 38 (5). Sage Publications Sage UK: London, England: 507–17.

Matez-Bandera, JL, J Monroy, and J Gonzalez-Jimenez. 2021. “Efficient Semantic Place Categorization by a Robot through Active Line-of-Sight Selection.” Knowledge-Based Systems. Elsevier, 108022.

Mishra, Ruchik, Yug Ajmera, Nikhil Mishra, and Arshad Javed. 2019. “Ego-Centric Framework for a Three-Wheel Omni-Drive Telepresence Robot.” In 2019 IEEE International Conference on Advanced Robotics and Its Social Impacts (ARSO), 281–86. IEEE.

Monroy, Javier, Jose-Raul Ruiz-Sarmiento, Francisco-Angel Moreno, Cipriano Galindo, and Javier Gonzalez-Jimenez. 2019. “Olfaction, Vision, and Semantics for Mobile Robots. Results of the IRO Project.” Sensors 19 (16). Multidisciplinary Digital Publishing Institute: 3488.

Moreno, Francisco-Angel, Javier Monroy, Jose-Raul Ruiz-Sarmiento, Cipriano Galindo, and Javier Gonzalez-Jimenez. 2020. “Automatic Waypoint Generation to Improve Robot Navigation through Narrow Spaces.” Sensors 20 (1). Multidisciplinary Digital Publishing Institute: 240.

Nakamura, Tomoaki, and Takayuki Nagai. 2017. “Ensemble-of-Concept Models for Unsupervised Formation of Multiple Categories.” IEEE Transactions on Cognitive and Developmental Systems 10 (4). IEEE: 1043–57.

Othman, Kamal. 2020. “Towards the Vision of a Social Robot in Every Home: A Navigation Strategy via Enhanced Subsumption Architecture.” Applied Sciences: School of Mechatronic Systems Engineering.

Pierre, Cyrille. 2020. “Localisation Coopérative Robuste de Robots Mobiles Par Mesure D’inter-Distance.” Université Clermont Auvergne.

Pire, Taihú, Mart\\’ın Mujica, Javier Civera, and Ernesto Kofman. 2019. “The Rosario Dataset: Multisensor Data for Localization and Mapping in Agricultural Environments.” The International Journal of Robotics Research 38 (6). SAGE Publications Sage UK: London, England: 633–41.

Qi, Xianyu, Wei Wang, Ziwei Liao, Xiaoyu Zhang, Dongsheng Yang, and Ran Wei. 2020. “Object Semantic Grid Mapping with 2D LiDAR and RGB-D Camera for Domestic Robot Navigation.” Applied Sciences 10 (17). Multidisciplinary Digital Publishing Institute: 5782.

Qu, Yuanhao, Minghao Yang, Jiaqing Zhang, Wu Xie, Baohua Qiang, and Jinlong Chen. 2021. “An Outline of Multi-Sensor Fusion Methods for Mobile Agents Indoor Navigation.” Sensors 21 (5). Multidisciplinary Digital Publishing Institute: 1605.

Roa-Borbolla, Arturo Getsemani, Antonio Marin-Hernandez, Uriel H Hernandez-Belmonte, Victor Ayala-Ramirez, and Karen Roa-F. 2018. “Realistic and Automatic Map Generator for Mobile Robots.” In 2018 International Conference on Mechatronics, Electronics and Automotive Engineering (ICMEAE), 50–55. IEEE.

Roa-Borbolla, Arturo G, Yara A Jimnez-Nieto, Gerardo I Martinez Espinosa, Jorge L Villa-Paniagua, Monica Ruiz-Martinez, and Rosa M Vega-Valera. 2020. “Algorithm Comparison between a\* and PRM on Indoor Fire Simulation.” In 2020 International Conference on Mechatronics, Electronics and Automotive Engineering (ICMEAE), 23–28. IEEE.

Ruiz-Sarmiento, Jose-Raul, Samuel-Felipe Baltanas, and Javier Gonzalez-Jimenez. 2021. “Jupyter Notebooks in Undergraduate Mobile Robotics Courses: Educational Tool and Case Study.” Applied Sciences 11 (3). Multidisciplinary Digital Publishing Institute: 917.

Ruiz-Sarmiento, Jose-Raul, Cipriano Galindo, and Javier Gonzalez-Jimenez. 2017. “Building Multiversal Semantic Maps for Mobile Robot Operation.” Knowledge-Based Systems 119: 257–72. <https://doi.org/10.1016/j.knosys.2016.12.016>.

Ruiz-Sarmiento, Jose-Raul, Cipriano Galindo, Javier Monroy, Francisco-Angel Moreno, and Javier Gonzalez-Jimenez. 2019. “Ontology-Based Conditional Random Fields for Object Recognition.” Knowledge-Based Systems 168. Elsevier: 100–108.

Ruiz-Sarmiento, J. R. 2016. “Probabilistic Techniques in Semantic Mapping for Mobile Robotics.” University of Málaga.

Ruiz-Sarmiento, J. R., Cipriano Galindo, and Javier González-Jiménez. 2017. “Robot@Home, a Robotic Dataset for Semantic Mapping of Home Environments.” International Journal of Robotics Research. <https://zenodo.org/record/4495821>.

Ruiz-Sarmiento, J.R., Javier Monroy, Francisco-Angel Moreno, and Javier González-Jiménez. 2020. “Tutorial Para El Reconocimiento de Objetos Basado En Características Empleando Herramientas Python.” In Conference: XXXIX Jornadas de Automática, 998–1005. <10.17979/spudc.9788497497565.0998>.

Ruiz-Sarmiento, JR, J Monroy, FA Moreno, and J Gonzalez-Jimenez. 2019. “A TUTORIAL on OBJECT RECOGNITION by MACHINE LEARNING TECHNIQUES USING PYTHON.” In Proceedings of INTED2019 Conference, 11th-13th March, Valencia.

Salhi, Imane. 2021. “Intelligent Embedded Camera for Robust Object Tracking on Mobile Platform.” Université Gustave Eiffel.

Setiono, Felix Yustian, Armagan Elibol, and Nak Young Chong. 2021. “A Novel Room Categorization Approach to Semantic Localization for Domestic Service Robots.” In 2021 21st International Conference on Control, Automation and Systems (ICCAS), 1166–71. IEEE.

Shu, Fangwen, Paul Lesur, Yaxu Xie, Alain Pagani, and Didier Stricker. 2021. “SLAM in the Field: An Evaluation of Monocular Mapping and Localization on Challenging Dynamic Agricultural Environment.” In Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision, 1761–71.

Suh, Hyung Ju. 2018. “Semantic Task Planning in Household Environments Using Temporal Logic Synthesis.” In Unknown.

Suveges, Tamas, and Stephen McKenna. 2021. “Egomap: Hierarchical First-Person Semantic Mapping.” In International Conference on Pattern Recognition, 348–63. Springer.

Tarifa, Jaimez, and others. 2017. “Motion Estimation, 3D Reconstruction and Navigation with Range Sensors.” Technische Universität München.

Yu, Liangjiang, and Guoliang Fan. 2021. “DrsNet: Dual-Resolution Semantic Segmentation with Rare Class-Oriented Superpixel Prior.” Multimedia Tools and Applications 80 (2). Springer: 1687–1706.

Zuñiga-Noël, David, Jose-Raul Ruiz-Sarmiento, and Javier Gonzalez-Jimenez. 2019. “Intrinsic Calibration of Depth Cameras for Mobile Robots Using a Radial Laser Scanner.” In International Conference on Computer Analysis of Images and Patterns, 659–71. Springer.

Zuñiga-Noël, David, Jose-Raul Ruiz-Sarmiento, Ruben Gomez-Ojeda, and Javier Gonzalez-Jimenez. 2019. “Automatic Multi-Sensor Extrinsic Calibration for Mobile Robots.” IEEE Robotics and Automation Letters 4 (3). IEEE: 2862–69.


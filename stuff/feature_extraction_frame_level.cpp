
/****************************************************************************
*						 Room categorization								*
*    				Copyright (C) 2014  J.R. Ruiz-Sarmiento					*
*																			*
*    This program is free software: you can redistribute it and/or modify	*
*    it under the terms of the GNU General Public License as published by	*
*    the Free Software Foundation, either version 3 of the License, or		*
*    (at your option) any later version.									*
*																			*
*    This program is distributed in the hope that it will be useful,		*
*    but WITHOUT ANY WARRANTY; without even the implied warranty of			*
*    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the			*
*    GNU General Public License for more details.							*
*																			*
*    You should have received a copy of the GNU General Public License		*
*    along with this program.  If not, see <http://www.gnu.org/licenses/>.	*
*																			*
****************************************************************************/

// Includes
#include <iostream>
#include <numeric>

#include <mrpt/utils.h>
#include <mrpt/opengl.h>
#include <mrpt/maps/CColouredPointsMap.h>
#include <mrpt/obs/CObservation3DRangeScan.h>
#include <mrpt/obs/CRawlog.h>
#include <mrpt/system/datetime.h>
#include <mrpt/maps/CSimplePointsMap.h>
#include <mrpt/slam/CICP.h>
#include <mrpt/gui/CDisplayWindowPlots.h>

#include "CPointCloudAdapters.h"
#include "CPlanesDetection.h"
#include "Models.h"

#include "includes_DataIO.h"

#include <pcl/point_types.h>
#include <pcl/point_cloud.h>
#include <pcl/filters/approximate_voxel_grid.h>
#include <pcl/io/pcd_io.h>	// Load point cloud from file
#include <pcl/filters/extract_indices.h>
#include <pcl/visualization/pcl_visualizer.h>
#include <pcl/features/feature.h>
#include <pcl/io/ply_io.h>
#include <pcl/filters/extract_indices.h>
#include <pcl/filters/statistical_outlier_removal.h>
//#include <pcl/point_types_conversion.h>
#include <pcl/features/moment_invariants.h>

#include <pcl/surface/convex_hull.h>
#include <pcl/filters/crop_hull.h>
#include <pcl/kdtree/kdtree_flann.h>

#include <pcl/common/common.h>

#include <pcl/visualization/cloud_viewer.h>

#include <pcl/people/hog.h>

#include <boost/filesystem/operations.hpp>

//
// Namespaces
//
using namespace std;
using namespace SORT::DataIO;
using namespace SORT::ObjectRecognition;
using namespace SORT::Adapters;

using namespace mrpt::opengl;
using namespace mrpt::math;
using namespace mrpt::poses; CPointCloudColouredPtr scenePointCloud;
using namespace mrpt::obs;
using namespace mrpt::system;
using namespace mrpt::maps;
using namespace mrpt::slam;
using namespace mrpt::gui;

size_t objectID = 0;   // Used for rooms and objects
size_t relationID = 0;
size_t obsID    = 0;

Eigen::Matrix4f transMat;

vector<string> v_objectTypes;
map<string,size_t> m_objectTypes;

// For ICP
CPose2D		initialPose(0.0f,0.0f,(float)DEG2RAD(0.0f));
bool        visualize2DResults = false;
CDisplayWindowPlotsPtr	win = CDisplayWindowPlotsPtr(new CDisplayWindowPlots("ICP results"));

// Data directories
string datasetPath   = "/home/raul/Storage/Raul Home/Dataset/";
string scenesDir     = "6 - Labeled Scenes/";
string rawlogsDir    = "";
string laserScansDir = "";

// Homes
vector<string> v_homes;

// Types of rooms

vector<string> v_typesOfRooms;


struct TLabelledBox
{
    // Loaded from .scene file
    CBoxPtr box;   // object containing the corners of the object's bounding box
    string  label; // e.g. scourer, bowl, or scourer_1, bowl_3 if working with instances
    // Computed
    pcl::PointCloud<pcl::PointXYZ>::Ptr convexHullCloud;
    vector<pcl::Vertices>   polygons;

    TLabelledBox() : convexHullCloud(new pcl::PointCloud<pcl::PointXYZ>())
    {}
};

struct TObject
{
    string label; // e.g. scourer, bowl, or scourer_1, bowl_3 if working with instances
    size_t ID;
    pcl::PointCloud<pcl::PointXYZRGB>::Ptr cloud;
    string type;
    size_t gt; // Ground trurth. An ID identifying the type of the object
    double planarity;
    double scatter;
    double linearity;
    double minHeight;
    double maxHeight;
    double centroid_x, centroid_y, centroid_z;
    double volume;
    double biggestArea;
    double orientation;
    double hueMean, satMean, valMean;
    double hueStdv, satStdv, valStdv;
    vector<double> hue_hist, val_hist, sat_hist; // Histograms for HSV values
    pcl::PointXYZ min_pt, max_pt;

    TObject() : cloud(new pcl::PointCloud<pcl::PointXYZRGB>)
    {}
};

struct TRelation
{
    size_t relationID;
    string label1, label2;
    size_t ID1, ID2;
    size_t gt1, gt2;
    vector<double> features;
};

struct TScan // 2D laser scan
{
    TTimeStamp      time;
    vector<double>  scanFeatures; // Features extracted from the scan
};

struct TObsContent
{
    string          sensorLabel; // The sensor that grabbed the observation
    size_t          ID;
    vector<size_t>  objects; // IDs of objects appearing in this observation
    vector<double>  roomFeatures; // Features extracted to characterize the room
    vector<double>  meanRoomFeatures;
    size_t          N_previousObs;
    TScan           scan;
};

boost::shared_ptr<pcl::visualization::PCLVisualizer>	viewer(new pcl::visualization::PCLVisualizer ("3D Viewer"));

//-----------------------------------------------------------
//                   getScenesToProcess
//-----------------------------------------------------------

void getScenesToProcess( string home, string roomType, vector<string> &v_scenes)
{
    bool roomExists = true;
    size_t sceneIndex = 1;
    size_t sarmisHome = ( home.find("sarmis") != std::string::npos) ? true : false ;
    size_t sarmisSceneSubIndex = 1;

    while ( roomExists )
    {
        std::stringstream sceneFileName;
        sceneFileName << datasetPath << scenesDir << home << "/"
                      << roomType << sceneIndex;

        if (sarmisHome)
        {
            sceneFileName << "_" << sarmisSceneSubIndex++ << "_labelled.scene";
        }
        else
            sceneFileName << "_labelled.scene";

        //cout << "    Checking existence of file: " << sceneFileName.str() << endl;

        if ( mrpt::system::fileExists(sceneFileName.str()) )
        {
            v_scenes.push_back(sceneFileName.str());

            if (!sarmisHome)
                sceneIndex++;
        }
        else
        {
            if (sarmisHome)
            {
                if ( sceneIndex < 3 )
                {
                    sceneIndex++;
                    sarmisSceneSubIndex = 1;
                }
                else
                    roomExists = false;
            }
            else
                roomExists = false;
        }
    }
}

//-----------------------------------------------------------
//                   showVectorContent
//-----------------------------------------------------------

void showVectorContent(const string &header,vector<string> &v, bool eol=false)
{
    cout << header;
    for (size_t i=0; i < v.size(); i++)
    {
        cout << v[i] << " ";
        if (eol) cout << endl;
    } cout << endl;
}

//-----------------------------------------------------------
//                   showVectorContent
//-----------------------------------------------------------

void showVectorContent(const string &header,vector<size_t> &v, bool eol=false)
{
    cout << header;
    for (size_t i=0; i < v.size(); i++)
    {
        cout << v[i] << " ";
        if (eol) cout << endl;
    } cout << endl;
}

//-----------------------------------------------------------
//                    getObjectGT
//-----------------------------------------------------------

size_t getObjectGT(const string &objType)
{
    for (size_t i_objType = 0; i_objType < v_objectTypes.size(); i_objType++ )
    {
        if (v_objectTypes[i_objType] == objType)
        {
            return i_objType;
        }
    }

    cerr << "  [ERROR] Object type unkwnown when retrieving its GT. Object type: " << objType << endl;

    return 0;
}

//-----------------------------------------------------------
//                    getObjectType
//-----------------------------------------------------------

string getObjectType(const string &label)
{
    string type;
    vector<string> tokens;

    mrpt::system::tokenize	(label,"_",tokens);

    for (size_t i_token = 0; i_token < tokens.size()-1; i_token++ )
    {
        if (i_token)
            type.append("_");

        type.append(tokens[i_token]);
    }

    return type;
}

//-----------------------------------------------------------
//                    getObjectID
//-----------------------------------------------------------

size_t getObjectID(const string &label, vector<TObject> &v_objects)
{
    for (size_t i_obj = 0; i_obj < v_objects.size(); i_obj++ )
    {
        if (v_objects[i_obj].label == label)
        {
            return v_objects[i_obj].ID;
        }
    }

    cerr << "  [ERROR] Object label unkwnown when retrieving its ID. Object label: " << label << endl;

    return 0;
}

//-----------------------------------------------------------
//                    getObjectType
//-----------------------------------------------------------

void insertObjectType(const string &type)
{
    // If not already inserted, insert it
    if ( find(v_objectTypes.begin(), v_objectTypes.end(), type) == v_objectTypes.end() )
    {
        v_objectTypes.push_back(type);
        m_objectTypes[type] = 1;
    }
    else
        m_objectTypes[type] = m_objectTypes[type] + 1;
}

//-----------------------------------------------------------
//                    loadLabelledScene
//-----------------------------------------------------------

void  loadLabelledScene(const string sceneFileName,
                        mrpt::opengl::COpenGLScenePtr labelledScene,
                        vector<TLabelledBox> &v_labelled_boxes,
                        vector<string>       &v_appearingLabels)
{
    if ( labelledScene->loadFromFile( sceneFileName ) )
    {
        bool keepLoading = true;
        size_t pointClouds_inserted = 0;

        while (keepLoading)
        {
            if (!pointClouds_inserted)
            {
                scenePointCloud = labelledScene->getByClass<CPointCloudColoured>(0);

            }
            else
            {
                CPointCloudColouredPtr auxPointCloud = labelledScene->getByClass<CPointCloudColoured>(pointClouds_inserted);

                if ( auxPointCloud.null() )
                    keepLoading = false;
                else
                {
                    for ( size_t i_point = 0; i_point < auxPointCloud->size(); i_point++ )
                    {
                        mrpt::opengl::CPointCloudColoured::TPointColour point = auxPointCloud->getPoint(i_point);
                        scenePointCloud->push_back(point.x, point.y, point.z,
                                                   point.R, point.G, point.B);
                    }
                }
            }

            pointClouds_inserted++;
        }



        // Load previously inserted boxes
        keepLoading = true;
        size_t boxes_inserted = 0;

        while ( keepLoading )
        {
            CBoxPtr box = labelledScene->getByClass<CBox>(boxes_inserted);

            if ( box.null() )
                keepLoading = false;
            else
            {
                TLabelledBox labelled_box;

                labelled_box.box = box;
                labelled_box.label = box->getName();

                if ( labelled_box.label.empty() || labelled_box.label == " " )
                    labelled_box.label = "unknown";

                TPose3D pose = box->getPose();

                TPoint3D c1,c2;
                box->getBoxCorners(c1,c2);

                TPoint3D C111 ( CPose3D(pose) + TPose3D(TPoint3D(c1.x,c1.y,c1.z)) );
                TPoint3D C112 ( CPose3D(pose) + TPose3D(TPoint3D(c1.x,c1.y,c2.z)) );
                TPoint3D C121 ( CPose3D(pose) + TPose3D(TPoint3D(c1.x,c2.y,c1.z)) );
                TPoint3D C122 ( CPose3D(pose) + TPose3D(TPoint3D(c1.x,c2.y,c2.z)) );
                TPoint3D C211 ( CPose3D(pose) + TPose3D(TPoint3D(c2.x,c1.y,c1.z)) );
                TPoint3D C212 ( CPose3D(pose) + TPose3D(TPoint3D(c2.x,c1.y,c2.z)) );
                TPoint3D C221 ( CPose3D(pose) + TPose3D(TPoint3D(c2.x,c2.y,c1.z)) );
                TPoint3D C222 ( CPose3D(pose) + TPose3D(TPoint3D(c2.x,c2.y,c2.z)) );

                pcl::PointCloud<pcl::PointXYZ>::Ptr pointCloud ( new pcl::PointCloud<pcl::PointXYZ>());
                pointCloud->push_back( pcl::PointXYZ( C111.x, C111.y, C111.z ));
                pointCloud->push_back( pcl::PointXYZ( C112.x, C112.y, C112.z ));
                pointCloud->push_back( pcl::PointXYZ( C121.x, C121.y, C121.z ));
                pointCloud->push_back( pcl::PointXYZ( C122.x, C122.y, C122.z ));
                pointCloud->push_back( pcl::PointXYZ( C211.x, C211.y, C211.z ));
                pointCloud->push_back( pcl::PointXYZ( C212.x, C212.y, C212.z ));
                pointCloud->push_back( pcl::PointXYZ( C221.x, C221.y, C221.z ));
                pointCloud->push_back( pcl::PointXYZ( C222.x, C222.y, C222.z ));

                pcl::ConvexHull<pcl::PointXYZ> convex_hull;
                convex_hull.setInputCloud(pointCloud);
                convex_hull.setDimension(3);
                convex_hull.reconstruct(*labelled_box.convexHullCloud,
                                        labelled_box.polygons);

                pcl::transformPointCloud( *labelled_box.convexHullCloud,
                                          *labelled_box.convexHullCloud,
                                          transMat );

                v_labelled_boxes.push_back( labelled_box );

                // Check if the label has been already inserted
                if ( find(v_appearingLabels.begin(),
                          v_appearingLabels.end(),
                          labelled_box.label) == v_appearingLabels.end() )
                    v_appearingLabels.push_back(labelled_box.label);

                // Insert the object type
                insertObjectType( getObjectType(labelled_box.label) );
            }

            boxes_inserted++;
        }

        cout << "  [INFO] " << v_labelled_boxes.size() <<  " labelled boxes loaded." << endl;

    }
    else
        cout << "  [ERROR] While loading the labelled scene file." << endl;

}

//-----------------------------------------------------------
//                      checkIsOn
//-----------------------------------------------------------

bool checkIsOn(TObject &obj1, TObject &obj2)
{
    double y_threshold = 0.05;

    if (( ( obj1.min_pt.y < obj2.max_pt.y ) && ( obj1.max_pt.y > obj2.max_pt.y ) )
            || ( obj1.min_pt.y - obj2.max_pt.y < y_threshold ) )
    {
        size_t N_points = obj1.cloud->points.size();
        size_t N_points_in = 0;
        for ( size_t point_index = 0; point_index < N_points; point_index += 3 )
        {
            pcl::PointXYZRGB &point = obj1.cloud->points[point_index];
            if ( ( obj2.max_pt.z > point.z ) && ( obj2.min_pt.z < point.z)
                 && ( obj2.max_pt.x > point.x ) && ( obj2.min_pt.x < point.x) )
                N_points_in++;
        }

        double ratio = (double)N_points_in / (double)(N_points/3);

        // 80% of points inside the other object projection
        if ( ratio > 0.8 )
            return true;
    }

    return false;
}

//-----------------------------------------------------------
//                     characterizeMap
//-----------------------------------------------------------

void characterizeMap(CSimplePointsMap &m1, TScan &scan)
{
    vector<double> &feats = scan.scanFeatures;

    pcl::PointCloud<pcl::PointXYZ>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZ>());
    pcl::PointCloud<pcl::PointXYZ>::Ptr rotated_cloud(new pcl::PointCloud<pcl::PointXYZ>());
    m1.getPCLPointCloud(*cloud);
    pcl::transformPointCloud(*cloud,*cloud,transMat);

    pcl::StatisticalOutlierRemoval<pcl::PointXYZ> sor;
    sor.setInputCloud (cloud);
    sor.setMeanK (50);
    sor.setStddevMulThresh (1.0);
    sor.filter (*cloud);

    // Compute principal directions
    // compute principal direction
    Eigen::Vector4f centroid;
    pcl::compute3DCentroid(*cloud, centroid);
    Eigen::Matrix3f covariance;
    computeCovarianceMatrixNormalized(*cloud, centroid, covariance);
    Eigen::SelfAdjointEigenSolver<Eigen::Matrix3f> eigen_solver(covariance, Eigen::ComputeEigenvectors);
    Eigen::Matrix3f eigDx = eigen_solver.eigenvectors();
    Eigen::Vector3f eigValues = eigen_solver.eigenvalues(); // eigValues(0) < eigValues(1) < eigValues(2)ç

    // Normalize
    double sumEV = eigValues(0) + eigValues(1) + eigValues(2);
    eigValues(0) /= sumEV;
    eigValues(1) /= sumEV;
    eigValues(2) /= sumEV;

    pcl::PointXYZ centroid1;
    centroid1.x = centroid(0);
    centroid1.y = centroid(1);
    centroid1.z = centroid(2);

    eigDx.col(2) = eigDx.col(1).cross(eigDx.col(0));

    Eigen::Matrix3f eigDxAux = eigDx;
    eigDx.col(0) = eigDxAux.col(1);

    if ( eigDxAux(1,0) < 0 )
        eigDx.col(1) = -eigDxAux.col(0);
    else
        eigDx.col(1) = eigDxAux.col(0);

    if ( eigDxAux(2,1) < 0 )
        eigDx.col(2) = -eigDx.col(0);
    else
        eigDx.col(2) = eigDx.col(0);

    if ( eigDxAux(0,2) > 0 )
        eigDx.col(0) = eigDxAux.col(2);
    else
        eigDx.col(0) = -eigDxAux.col(2);

    // move the points to the that reference frame
    Eigen::Matrix4f p2w(Eigen::Matrix4f::Identity());
    p2w.block<3,3>(0,0) = eigDx.transpose();
    p2w.block<3,1>(0,3) = -1.f * (p2w.block<3,3>(0,0) * centroid.head<3>());

    pcl::transformPointCloud(*cloud, *rotated_cloud, p2w);

    pcl::PointXYZ min_pt, max_pt;
    pcl::getMinMax3D(*rotated_cloud, min_pt, max_pt);

    double y_dist = ( max_pt.y > 0 )
            ? (( min_pt.y > 0 )
               ? (max_pt.y - min_pt.y)		// Both positive
               : (max_pt.y + abs(min_pt.y)))	// Up positive and down negative
            : abs(max_pt.y) - abs(min_pt.y);	// Both negative

    double x_dist = ( max_pt.x > 0 )
            ? (( min_pt.x > 0 )
               ? (max_pt.x - min_pt.x)		// Both positive
               : (max_pt.x + abs(min_pt.x)))	// Up positive and down negative
            : abs(max_pt.x) - abs(min_pt.x);	// Both negative

    double z_dist = ( max_pt.z > 0 )
            ? (( min_pt.z > 0 )
               ? (max_pt.z - min_pt.z)		// Both positive
               : (max_pt.z + abs(min_pt.z)))	// Up positive and down negative
            : abs(max_pt.z) - abs(min_pt.z);	// Both negative

    double area = x_dist*z_dist;

    double elongation = ( x_dist > z_dist ) ? x_dist/z_dist : z_dist/x_dist;

    double minDistance = std::numeric_limits<double>::max();
    double maxDistance = -std::numeric_limits<double>::max();
    double distance = 0;
    for ( size_t i = 0; i < cloud->points.size(); i++ )
    {
        pcl::PointXYZ &point = cloud->points[i];
        double dist = sqrt(pow(point.x,2)+pow(point.y,2)+pow(point.z,2));
        distance += dist;

        if ( dist < minDistance ) minDistance = dist;
        if ( dist > maxDistance ) maxDistance = dist;
    }
    double meanDistance = distance / (float) cloud->points.size();

    double acc = 0;
    for ( size_t i = 0; i < cloud->points.size(); i++ )
    {
        pcl::PointXYZ &point = cloud->points[i];
        acc += pow( sqrt(pow(point.x,2)+pow(point.y,2)+pow(point.z,2)) - meanDistance,2);
    }

    double distanceStdv = sqrt(acc / cloud->points.size() );

    double numOfPoints = cloud->points.size();
    double compactness = maxDistance / minDistance;
    double compactness2 = maxDistance / meanDistance;

    //
    // COMPUTE LINEARITY

    double linearity = eigValues(2) - eigValues(1);

    //
    // COMPUTE SCATTER

    double scatter = eigValues(2);

    //    cout << "Area      : " << area << endl;
    //    cout << "Elongation: " << elongation << endl;
    //    cout << "Mean dist : " << meanDistance << endl;
    //    cout << "Dist. stdv: " << distanceStdv << endl;
    //    cout << "Num points: " << numOfPoints << endl;
    //    cout << "Compact   : " << compactness << endl;
    //    cout << "Compact2  : " << compactness2 << endl;
    //    cout << "Linearity : " << linearity << endl;
    //    cout << "Scatter   : " << scatter << endl;

    feats.push_back(area);
    feats.push_back(elongation);
    feats.push_back(meanDistance);
    feats.push_back(distanceStdv);
    feats.push_back(numOfPoints);
    feats.push_back(compactness);
    feats.push_back(compactness2);
    feats.push_back(linearity);
    feats.push_back(scatter);

    //    viewer->resetStoppedFlag();
    //    viewer->addPointCloud( rotated_cloud );

    //    while (!viewer->wasStopped())
    //    {
    //        viewer->spinOnce(100);
    //    }

    //    viewer->removeAllPointClouds();
}

//-----------------------------------------------------------
//                    characterizeObs
//-----------------------------------------------------------

void characterizeObs( TObsContent &obsContent,
                      CObservation3DRangeScanPtr obs,
                      TObsContent *prevObs)
{
    // CHECK VALID OBS

    // Convert into PCL point cloud format

    pcl::PointCloud<pcl::PointXYZ>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZ>());
    obs->project3DPointsFromDepthImageInto(*cloud,false);

    // Transform point cloud from MRPT to PCL coordinate system
    pcl::transformPointCloud( *cloud, *cloud, transMat );

    // Valid obs?
    if ( cloud->points.size() == 0 )
        return;

    // GET HSV RELATED FEATURES
    //
    size_t width = obs->intensityImage.getWidth();
    size_t height = obs->intensityImage.getHeight();

    vector<double> v_hue, v_sat, v_val;

    for ( size_t row = 0; row < height; row++ )
        for ( size_t col = 0; col < width; col++ )
        {
            float r,g,b,h,s,v;
            r = obs->intensityImage.getAsFloat(col,row,0);
            g = obs->intensityImage.getAsFloat(col,row,1);
            b = obs->intensityImage.getAsFloat(col,row,2);

            mrpt::utils::rgb2hsv(r,g,b,h,s,v);

            if ( h > 1 )
                h = 1;

            v_hue.push_back(h);
            v_sat.push_back(s);
            v_val.push_back(v);
        }

    double sum = std::accumulate(v_hue.begin(), v_hue.end(), 0.0);
    double hueMean = sum / v_hue.size();

    double acc = 0;
    for ( size_t i = 0; i < v_hue.size(); i++ )
        acc += pow(v_hue[i]-hueMean,2);

    double hueStdv = sqrt(acc / v_hue.size() );

    sum = std::accumulate(v_val.begin(), v_val.end(), 0.0);
    double valMean = sum / v_val.size();

    acc = 0;
    for ( size_t i = 0; i < v_val.size(); i++ )
        acc += pow(v_val[i]-valMean,2);

    double valStdv = sqrt(acc / v_val.size() );

    sum = std::accumulate(v_sat.begin(), v_sat.end(), 0.0);
    double satMean = sum / v_sat.size();

    acc = 0;
    for ( size_t i = 0; i < v_sat.size(); i++ )
        acc += pow(v_sat[i]-satMean,2);

    double satStdv = sqrt(acc / v_sat.size() );

    // COMPUTE HISTOGRAMS
    //
    // 8 bins per histogram. Saturation [0..1] Hue [0..?] Value [0..1]

    size_t N_bins = 5;
    double hue_binSize = 1.0001/(double)N_bins;
    double val_binSize = 1.0001/(double)N_bins;
    double sat_binSize = 1.0001/(double)N_bins;

    vector<double> hue_hist(N_bins), val_hist(N_bins), sat_hist(N_bins);

    size_t N_points = v_hue.size(); // N_pixels

    for ( size_t i_point = 0; i_point < N_points ; i_point++ )
    {
        double hue = v_hue[i_point];
        double val = v_val[i_point];
        double sat = v_sat[i_point];

        //        cout << floor(hue/hue_binSize) << " " << floor(val/val_binSize)<< " " << floor(sat/sat_binSize) << endl;
        hue_hist[floor(hue/hue_binSize)]++;
        val_hist[floor(val/val_binSize)]++;
        sat_hist[floor(sat/sat_binSize)]++;
    }

    // Normalize histograms

    for ( size_t i_bin = 0; i_bin < N_bins; i_bin++ )
    {
        hue_hist[i_bin] = hue_hist[i_bin]/(float)N_points;
        val_hist[i_bin] = val_hist[i_bin]/(float)N_points;
        sat_hist[i_bin] = sat_hist[i_bin]/(float)N_points;
    }

    obsContent.roomFeatures.push_back(hueMean);
    obsContent.roomFeatures.push_back(satMean);
    obsContent.roomFeatures.push_back(valMean);

    obsContent.roomFeatures.push_back(hueStdv);
    obsContent.roomFeatures.push_back(satStdv);
    obsContent.roomFeatures.push_back(valStdv);

    for ( size_t i_bin = 0; i_bin < N_bins; i_bin++ )
        obsContent.roomFeatures.push_back(hue_hist[i_bin]);

    for ( size_t i_bin = 0; i_bin < N_bins; i_bin++ )
        obsContent.roomFeatures.push_back(sat_hist[i_bin]);

    for ( size_t i_bin = 0; i_bin < N_bins; i_bin++ )
        obsContent.roomFeatures.push_back(val_hist[i_bin]);

    // GET GEOMETRIC FEATURES
    //

    // GET MEAN DISTANCE OF THE OBS

    Eigen::Vector4f centroid;
    pcl::compute3DCentroid(*cloud, centroid);
    double distance = sqrt( pow(centroid(0),2) + pow(centroid(1),2) + pow(centroid(2),2));

    obsContent.roomFeatures.push_back(distance);

    // GET THE SCENE FOOTPRINT

    pcl::PointXYZ min_pt, max_pt;
    pcl::getMinMax3D(*cloud, min_pt, max_pt);

    double x_dist = ( max_pt.x > 0 )
            ? (( min_pt.x > 0 )
               ? (max_pt.x - min_pt.x)		// Both positive
               : (max_pt.x + abs(min_pt.x)))	// Up positive and down negative
            : abs(max_pt.x) - abs(min_pt.x);	// Both negative

    double z_dist = ( max_pt.z > 0 )
            ? (( min_pt.z > 0 )
               ? (max_pt.z - min_pt.z)		// Both positive
               : (max_pt.z + abs(min_pt.z)))	// Up positive and down negative
            : abs(max_pt.z) - abs(min_pt.z);	// Both negative

    double footPrint = x_dist*z_dist;

    obsContent.roomFeatures.push_back(footPrint);

    // GET SCENE VOLUME

    double y_dist = ( max_pt.y > 0 )
            ? (( min_pt.y > 0 )
               ? (max_pt.y - min_pt.y)		// Both positive
               : (max_pt.y + abs(min_pt.y)))	// Up positive and down negative
            : abs(max_pt.y) - abs(min_pt.y);	// Both negative

    double volume = x_dist*z_dist*y_dist;

    obsContent.roomFeatures.push_back(volume);

    // COMPUTE MEAN FEATURES

    if (prevObs)
    {
        vector<double> &meanFeats = prevObs->meanRoomFeatures;
        vector<double> &feats     = obsContent.roomFeatures;
        size_t         N_prev     = prevObs->N_previousObs;

        obsContent.N_previousObs = N_prev+1;

        for ( size_t i_feat = 0; i_feat < feats.size(); i_feat++ )
            obsContent.meanRoomFeatures.push_back((feats[i_feat]+meanFeats[i_feat]*N_prev)/(N_prev+1));

    }
    else // This is the first obs
    {
        obsContent.meanRoomFeatures = obsContent.roomFeatures;
        obsContent.N_previousObs = 1;
    }
}


//-----------------------------------------------------------
//                   characterizeObject
//-----------------------------------------------------------

void characterizeObject( TObject &obj )
{
    size_t N_points = obj.cloud->points.size();

    vector<double> v_hueValues,v_valValues, v_satValues;

    // Check if the object has points
    if ( !N_points ) return;

    // COMPUTE HSV FEATS
    //

    // Get point cloud without colors
    for ( size_t i_point = 0; i_point < N_points ; i_point++ )
    {
        pcl::PointXYZHSV hsv;
        SORT::ObjectRecognition::pointRGBtoHSV(obj.cloud->points[i_point], hsv);
        v_hueValues.push_back( hsv.h );
        v_valValues.push_back( hsv.v );
        v_satValues.push_back( hsv.s );
    }

    // MEAN AND STDVS

    double sum = std::accumulate(v_hueValues.begin(), v_hueValues.end(), 0.0);
    obj.hueMean = sum / v_hueValues.size();

    double acc = 0;
    for ( size_t i = 0; i < v_hueValues.size(); i++ )
        acc += pow(v_hueValues[i]-obj.hueMean,2);

    obj.hueStdv = sqrt(acc / v_hueValues.size() );

    sum = std::accumulate(v_valValues.begin(), v_valValues.end(), 0.0);
    obj.valMean = sum / v_valValues.size();

    acc = 0;
    for ( size_t i = 0; i < v_valValues.size(); i++ )
        acc += pow(v_valValues[i]-obj.valMean,2);

    obj.valStdv = sqrt(acc / v_valValues.size() );

    sum = std::accumulate(v_satValues.begin(), v_satValues.end(), 0.0);
    obj.satMean = sum / v_satValues.size();

    acc = 0;
    for ( size_t i = 0; i < v_satValues.size(); i++ )
        acc += pow(v_satValues[i]-obj.satMean,2);

    obj.satStdv = sqrt(acc / v_satValues.size() );

    // COMPUTE HISTOGRAMS
    //
    // 8 bins per histogram. Saturation [0..1] Hue [0..360] Value [0..1]

    size_t N_bins = 5;
    double hue_binSize = 361/(double)N_bins;
    double val_binSize = 1.0001/(double)N_bins;
    double sat_binSize = 1.0001/(double)N_bins;

    obj.hue_hist.resize(N_bins);
    obj.val_hist.resize(N_bins);
    obj.sat_hist.resize(N_bins);

    for ( size_t i_point = 0; i_point < N_points ; i_point++ )
    {
        double hue = v_hueValues[i_point];
        double val = v_valValues[i_point];
        double sat = v_satValues[i_point];

        //        cout << floor(hue/hue_binSize) << " " << floor(val/val_binSize)<< " " << floor(sat/sat_binSize) << endl;

        obj.hue_hist[floor(hue/hue_binSize)]++;
        obj.val_hist[floor(val/val_binSize)]++;
        obj.sat_hist[floor(sat/sat_binSize)]++;
    }

    // Normalize histograms

    for ( size_t i_bin = 0; i_bin < N_bins; i_bin++ )
    {
        obj.hue_hist[i_bin] = obj.hue_hist[i_bin]/(float)N_points;
        obj.val_hist[i_bin] = obj.val_hist[i_bin]/(float)N_points;
        obj.sat_hist[i_bin] = obj.sat_hist[i_bin]/(float)N_points;
    }

    // Get point cloud without colors
    pcl::PointCloud<pcl::PointXYZ>::Ptr object_pcXYZ(new pcl::PointCloud<pcl::PointXYZ>);
    pcl::copyPointCloud(*obj.cloud,*object_pcXYZ);

    //
    // COMPUTE ORIENTATION

    // compute principal direction
    Eigen::Vector4f centroid;
    pcl::compute3DCentroid(*object_pcXYZ, centroid);
    Eigen::Matrix3f covariance;
    pcl::computeCovarianceMatrixNormalized(*object_pcXYZ, centroid, covariance);
    Eigen::SelfAdjointEigenSolver<Eigen::Matrix3f> eigen_solver(covariance, Eigen::ComputeEigenvectors);
    Eigen::Matrix3f eigDx = eigen_solver.eigenvectors();
    Eigen::Vector3f eigValues = eigen_solver.eigenvalues(); // eigValues(0) < eigValues(1) < eigValues(2)

    pcl::PointXYZ centroid1;
    centroid1.x = centroid(0);
    centroid1.y = centroid(1);
    centroid1.z = centroid(2);

    obj.centroid_x = centroid1.x;
    obj.centroid_y = centroid1.y; // height
    obj.centroid_z = centroid1.z;


    eigDx.col(2) = eigDx.col(1).cross(eigDx.col(0));

    // Angle between two vectors: acos( scalarproduct(v1,v2) / |v1||v2| )
    // In this case |v1| and |v2| = 1

    float scalarProduct = eigDx(0,0)*0 + eigDx(1,0)*1 + eigDx(2,0)*0;
    float teta = acos(scalarProduct);

    float tetaInDegrees = teta*(180.0 / 3.14159265);

    // Check if the result is a NaN
    if ( ( tetaInDegrees >= 0 ) && ( tetaInDegrees <= 180 ) )
    {
        if ( tetaInDegrees > 90 )
            tetaInDegrees = 90 - (tetaInDegrees -90);

        obj.orientation = (double)tetaInDegrees;
    }
    else
        obj.orientation = 0;

    // Normalize
    double sumEV = eigValues(0) + eigValues(1) + eigValues(2);
    eigValues(0) /= sumEV;
    eigValues(1) /= sumEV;
    eigValues(2) /= sumEV;

    //
    // COMPUTE PLANARITY

    obj.planarity = eigValues(1) - eigValues(0);

    //
    // COMPUTE LINEARITY

    obj.linearity = eigValues(2) - eigValues(1);

    //
    // COMPUTE SCATTER

    obj.scatter = eigValues(2);

    //
    // COMPUTE MIN AND MAX HEIGHT FROM THE FLOOR

    pcl::PointXYZ min_pt, max_pt;
    pcl::getMinMax3D(*object_pcXYZ, min_pt, max_pt);
    obj.min_pt = min_pt;
    obj.max_pt = max_pt;

    obj.minHeight = min_pt.y;
    obj.maxHeight = max_pt.y;

    if ( obj.type == "cabinet"  && ( obj.minHeight > 1) )
        obj.type = "upper_cabinet";

    //
    // COMPUTE VOLUME

    // move the points to the that reference frame
    Eigen::Matrix4f p2w(Eigen::Matrix4f::Identity());
    p2w.block<3,3>(0,0) = eigDx.transpose();
    p2w.block<3,1>(0,3) = -1.f * (p2w.block<3,3>(0,0) * centroid.head<3>());
    pcl::PointCloud<pcl::PointXYZ> cPoints;
    pcl::transformPointCloud(*object_pcXYZ, cPoints, p2w);

    pcl::getMinMax3D(cPoints, min_pt, max_pt);

    double y_dist = ( max_pt.y > 0 )
            ? (( min_pt.y > 0 )
               ? (max_pt.y - min_pt.y)		// Both positive
               : (max_pt.y + abs(min_pt.y)))	// Up positive and down negative
            : abs(max_pt.y) - abs(min_pt.y);	// Both negative

    double x_dist = ( max_pt.x > 0 )
            ? (( min_pt.x > 0 )
               ? (max_pt.x - min_pt.x)		// Both positive
               : (max_pt.x + abs(min_pt.x)))	// Up positive and down negative
            : abs(max_pt.x) - abs(min_pt.x);	// Both negative

    double z_dist = ( max_pt.z > 0 )
            ? (( min_pt.z > 0 )
               ? (max_pt.z - min_pt.z)		// Both positive
               : (max_pt.z + abs(min_pt.z)))	// Up positive and down negative
            : abs(max_pt.z) - abs(min_pt.z);	// Both negative

    obj.volume = y_dist*x_dist*z_dist;

    //
    // COMPUTE BIGGEST AREA

    double biggest_area = y_dist*x_dist;

    if ( y_dist*z_dist > biggest_area ) biggest_area = y_dist*z_dist;
    if ( x_dist*z_dist > biggest_area ) biggest_area = x_dist*z_dist;

    obj.biggestArea = biggest_area;
}

//-----------------------------------------------------------
//                  characterizeRelations
//-----------------------------------------------------------

void characterizeRelations(vector<TObject> &v_objects, vector<TRelation> &v_relations)
{
    // Iterate over all the objects in the scene
    for ( size_t i_obj = 0; i_obj < v_objects.size(); i_obj++ )
    {
        TObject &obj1 = v_objects[i_obj];

        // Check if the object has points
        if ( !obj1.cloud->size() || isNaN(obj1.planarity) ) continue;

        pcl::KdTreeFLANN<pcl::PointXYZ> kdtree;
        pcl::PointCloud<pcl::PointXYZ>::Ptr cloudXYZ(new pcl::PointCloud<pcl::PointXYZ>());
        pcl::copyPointCloud(*(obj1.cloud),*cloudXYZ);
        kdtree.setInputCloud (cloudXYZ);

        // Iterate over all the objects in the scene that can be neighbors of obj1
        for ( int j_obj = i_obj+1; j_obj < v_objects.size(); j_obj++ )
        {
            TObject &obj2 = v_objects[j_obj];

            // Check if the object has points
            if ( !obj2.cloud->size() || isNaN(obj1.planarity) ) continue;

            //            cout << "Analyzing " << obj1.label << " " << obj1.centroidHeight << " "
            //                 << obj2.label << " " << obj2.centroidHeight;

            double minDistance = 100000;
            bool related = false;

            // Check if their are near
            for ( size_t point_index = 0; point_index < obj2.cloud->points.size(); point_index += 3 )
            {
                size_t K = 3;

                pcl::PointXYZRGB &point = obj2.cloud->points[point_index];
                pcl::PointXYZ searchPoint;

                searchPoint.x = point.x;
                searchPoint.y = point.y;
                searchPoint.z = point.z;

                std::vector<int> pointIdxNKNSearch(K);
                std::vector<float> pointNKNSquaredDistance(K);

                /*std::cout << "K nearest neighbor search at (" << searchPoint.x
                            << " " << searchPoint.y
            << " " << searchPoint.z
            << ") with K=" << K << std::endl;*/

                if ( kdtree.nearestKSearch (searchPoint, K, pointIdxNKNSearch, pointNKNSquaredDistance) > 0 )
                {
                    //pcl::PointXYZRGB &point = o1.m_pointCloud->points[pointIdxNKNSearch[0]];
                    //cout << "D0: " << pointNKNSquaredDistance[0] << endl;
                    //cout << "D1: " << pointNKNSquaredDistance[1] << endl;
                    //cout << "D2: " << pointNKNSquaredDistance[2] << endl;
                    if ( sqrt(pointNKNSquaredDistance[2]) < minDistance )
                        minDistance = sqrt(pointNKNSquaredDistance[2]);
                }

                // A threshold of 0.3 m
                if ( minDistance < 150 ) // 150 meters (all the objects are neighbors :)
                {
                    //                    cout << " min distance: " << minDistance << endl;

                    // Perpendicularity
                    double perpendicularity = abs(obj1.orientation-obj2.orientation);
                    double v_distance       = abs(obj1.minHeight - obj2.minHeight);
                    double volumeRatio      = ( obj1.volume > obj2.volume ) ? obj1.volume / obj2.volume : obj2.volume / obj1.volume;
                    double isOn             =  ( checkIsOn(obj1,obj2) || checkIsOn(obj2,obj1) ) ? 1 : 0;

                    TRelation relation;

                    relation.label1 = obj1.label;
                    relation.label2 = obj2.label;
                    relation.relationID = relationID++;
                    relation.gt1 = obj1.gt;
                    relation.gt2 = obj2.gt;
                    relation.ID1 = obj1.ID;
                    relation.ID2 = obj2.ID;

                    relation.features.push_back(minDistance);
                    relation.features.push_back(perpendicularity);
                    relation.features.push_back(v_distance);
                    relation.features.push_back(volumeRatio);
                    relation.features.push_back(isOn);
                    relation.features.push_back(abs(obj1.hueStdv-obj2.hueStdv));
                    relation.features.push_back(abs(obj1.satStdv-obj2.satStdv));
                    relation.features.push_back(abs(obj1.valStdv-obj2.valStdv));
                    relation.features.push_back(abs(obj1.hueMean-obj2.hueMean));
                    relation.features.push_back(abs(obj1.satMean-obj2.satMean));
                    relation.features.push_back(abs(obj1.valMean-obj2.valMean));

                    v_relations.push_back(relation);

                    related = true;

                    break;
                }
            }
        }
    }
}

//-----------------------------------------------------------
//                  convertMRPTsceneToPCL
//-----------------------------------------------------------

void convertMRPTsceneToPCL(pcl::PointCloud<pcl::PointXYZRGB>::Ptr cloud,
                           pcl::PointCloud<pcl::PointXYZ>::Ptr auxCloud )
{
    // Convert into PCL point cloud format


    for ( size_t i_point = 0; i_point < scenePointCloud->size(); i_point++ )
    {
        mrpt::opengl::CPointCloudColoured::TPointColour point = scenePointCloud->getPoint(i_point);

        pcl::PointXYZRGB pcl_point(uint8_t(point.R*255),uint8_t(point.G*255),uint8_t(point.B*255));
        pcl_point.x = point.x;
        pcl_point.y = point.y;
        pcl_point.z = point.z;

        pcl::PointXYZ pcl_simple_point;
        pcl_simple_point.x = point.x;
        pcl_simple_point.y = point.y;
        pcl_simple_point.z = point.z;

        auxCloud->push_back(pcl_simple_point);
        cloud->push_back(pcl_point);
    }

    // Transform point cloud from MRPT to PCL coordinate system
    pcl::transformPointCloud( *cloud, *cloud, transMat );
    pcl::transformPointCloud( *auxCloud, *auxCloud, transMat );

    cout << "Done!" << endl;

//    viewer->addPointCloud( cloud );

//    while (!viewer->wasStopped())
//    {
//        viewer->spinOnce(100);
//    }

//    viewer->removeAllPointClouds();
//    viewer->resetStoppedFlag();
}


//-----------------------------------------------------------
//                  convertMRPTobsToPCL
//-----------------------------------------------------------

void convertMRPTobsToPCL(CObservation3DRangeScanPtr obs,
                         pcl::PointCloud<pcl::PointXYZ>::Ptr cloud )
{

}

//-----------------------------------------------------------
//                  extractObjectsFromScene
//-----------------------------------------------------------

void extractObjectsFromScene(vector<TLabelledBox> &v_labelled_boxes,
                             vector<TObject> &v_objects,
                             pcl::PointCloud<pcl::PointXYZRGB>::Ptr cloud,
                             pcl::PointCloud<pcl::PointXYZ>::Ptr auxCloud)
{
    for ( size_t i_box = 0; i_box < v_labelled_boxes.size(); i_box++ )
    {
        TLabelledBox &box = v_labelled_boxes[i_box];

        //cout << "Evaluating " << box.label;

        pcl::PointCloud<pcl::PointXYZ>::Ptr outputCloud(new pcl::PointCloud<pcl::PointXYZ>());
        pcl::CropHull<pcl::PointXYZ> cropHull;

        cropHull.setInputCloud( auxCloud );
        //cropHull.setIndices( boost::make_shared<const pcl::PointIndices> (indices) );
        cropHull.setHullIndices(box.polygons);
        cropHull.setHullCloud(box.convexHullCloud);
        cropHull.setDim(3);

        vector<int>     v_indices;

        cropHull.filter(v_indices);

        // Create the filtering object
        pcl::ExtractIndices<pcl::PointXYZRGB> extract;
        pcl::PointCloud<pcl::PointXYZRGB>::Ptr objectCloud(new pcl::PointCloud<pcl::PointXYZRGB>);

        // Extract the inliers
        extract.setInputCloud (cloud);
        boost::shared_ptr<vector<int> > pointIndices (new vector<int> (v_indices)); ;
        extract.setIndices (pointIndices);
        extract.setNegative (false);
        extract.filter (*objectCloud);

        cout << "     Filtering object " << box.label << " ..." ;
        //cropHull.filter(*outputCloud);
        cout << "Done! Number of points of the object: " << objectCloud->size();

        // Check if a previous part of this object was previously added
        //
        bool alreadyAdded = false;
        for ( size_t i_obj = 0; i_obj < v_objects.size(); i_obj++ )
            if ( v_objects[i_obj].label == box.label )
            {
                alreadyAdded = true;
                for ( size_t i_point = 0; i_point < objectCloud->points.size(); i_point++ )
                    v_objects[i_obj].cloud->points.push_back(objectCloud->points[i_point]);
            }

        if ( !alreadyAdded )
        {
            TObject newObj;
            newObj.label = box.label;
            pcl::copyPointCloud(*objectCloud,*newObj.cloud);

            newObj.type = getObjectType(newObj.label);
            newObj.gt   = getObjectGT(newObj.type);

            cout << " type : " << newObj.type << endl;

            newObj.ID = objectID++;

            v_objects.push_back(newObj);
        }

        //                    viewer->resetStoppedFlag();
        //                    viewer->addPointCloud( v_objects[v_objects.size()-1].cloud, mrpt::format("Object_%zu",i_box) );

        //                    while (!viewer->wasStopped())
        //                    {
        //                        viewer->spinOnce(100);
        //                    }

        //                    viewer->removeAllPointClouds();
    }

}

//-----------------------------------------------------------
//                        doICP
//-----------------------------------------------------------

void doICP(CSimplePointsMap &m1, CObservation2DRangeScanPtr obs2D, CDisplayWindowPlotsPtr win)
{
    CSimplePointsMap		m2;

    CICP::TReturnInfo		info;
    CICP					ICP;
    float                  runningTime;

    m2.insertObservation( obs2D.pointer() );

    // -----------------------------------------------------
    ICP.options.ICP_algorithm = icpLevenbergMarquardt;
    //ICP.options.ICP_algorithm = icpClassic;

    ICP.options.maxIterations			= 800;
    ICP.options.thresholdAng			= DEG2RAD(10.0f);
    ICP.options.thresholdDist			= 0.75f;
    ICP.options.ALFA					= 0.99f;
    ICP.options.smallestThresholdDist	= 0.05f;
    ICP.options.doRANSAC = true;

    //    ICP.options.dumpToConsole();
    // -----------------------------------------------------

    CPosePDFPtr pdf = ICP.Align(
                &m1,
                &m2,
                initialPose,
                &runningTime,
                (void*)&info);

    //    printf("    ICP run in %.02fms, %d iterations (%.02fms/iter), %.01f%% goodness\n    -> ",
    //           runningTime*1000,
    //           info.nIterations,
    //           runningTime*1000.0f/info.nIterations,
    //           info.goodness*100 );

    //    cout << "Mean of estimation: " << pdf->getMeanVal() << endl<< endl;
    if ( info.goodness < 0.7 )
        return;

    initialPose = pdf->getMeanVal();

    CPosePDFGaussian  gPdf;
    gPdf.copyFrom(*pdf);

    CSimplePointsMap m2_trans = m2;
    m2_trans.changeCoordinatesReference( gPdf.mean );

    m1.fuseWith(&m2_trans);

    if (visualize2DResults)
    {
        CMatrixFloat COV22 =  CMatrixFloat( CMatrixDouble( gPdf.cov ));
        COV22.setSize(2,2);
        Eigen::Vector2f MEAN2D(2);
        MEAN2D(0) = gPdf.mean.x();
        MEAN2D(1) = gPdf.mean.y();

        // Reference map:
        vector<float>   map1_xs, map1_ys, map1_zs;
        m1.getAllPoints(map1_xs,map1_ys,map1_zs);
        win->plot( map1_xs, map1_ys, "b.3", "map1");

        // Translated map:
        vector<float>   map2_xs, map2_ys, map2_zs;
        m2_trans.getAllPoints(map2_xs,map2_ys,map2_zs);
        win->plot( map2_xs, map2_ys, "r.3", "map2");

        // Uncertainty
        win->plotEllipse(MEAN2D(0),MEAN2D(1),COV22,3.0,"b2", "cov");

        win->axis(-1,10,-6,6);
        win->axis_equal();

        /*cout << "Close the window to exit" << endl;
            win->waitForKey();*/
        mrpt::system::sleep(1000);
    }
}

//-----------------------------------------------------------
//                      processScans
//-----------------------------------------------------------

void processScans( const string &sceneFileName, vector<TScan> &v_scans )
{
    CFileGZInputStream i_rawlog;

    // Check input rawlog file

    string rawlogFileName = "/";
    vector<string> tokens;

    mrpt::system::tokenize	(sceneFileName,"/",tokens);

    for (size_t i_token = 0; i_token < tokens.size()-3; i_token++ )
        rawlogFileName.append(tokens[i_token]+"/");

    rawlogFileName.append("1 - Raw data/");
    rawlogFileName.append(tokens[tokens.size()-2]+"/");
    rawlogFileName.append(tokens[tokens.size()-1].substr(0,tokens[tokens.size()-1].size()-15)+".rawlog");

    if (!mrpt::system::fileExists(rawlogFileName))
    {
        cerr << "  [ERROR] A rawlog file with name " << rawlogFileName;
        cerr << " doesn't exist." << endl;
        // return;
    }

    i_rawlog.open(rawlogFileName);

    cout << "  [INFO] Scans rawlog file   : " << rawlogFileName << endl;

    //
    // Process rawlog

    CActionCollectionPtr action;
    CSensoryFramePtr observations;
    CObservationPtr obs;
    size_t obsIndex = 0;

    bool first = true;

    cout.flush();

    CSimplePointsMap m1;

    while ( CRawlog::getActionObservationPairOrObservation(i_rawlog,action,observations,obs,obsIndex) )
    {

        // Check that it is a 2D observation
        if ( !IS_CLASS(obs, CObservation2DRangeScan) )
            continue;

        CObservation2DRangeScanPtr obs2D = CObservation2DRangeScanPtr(obs);

        TScan scan;
        scan.time = obs2D->timestamp;

        if ( first )
        {
            first = false;
            m1.insertObservation( obs2D.pointer() );
        }
        else
        {
            // do ICP with previous scans!
            doICP(m1, obs2D, win);
        }

        characterizeMap(m1,scan);
        v_scans.push_back(scan);
    }

    //TScan scan;
    //characterizeMap(m1,scan);
}

//-----------------------------------------------------------
//                      processRawlog
//-----------------------------------------------------------

void processRawlog( const string &sceneFileName,
                    vector<TObsContent> &v_obsContent,
                    vector<TObject> v_objects )
{
    CFileGZInputStream i_rawlog;

    // FIRST OF ALL, COMPUTE THE CHARACTERITSTICS FROM THE 2D SCANS
    //
    vector<TScan> v_scans;
    processScans( sceneFileName, v_scans );

    // Check input rawlog file

    string rawlogFileName = "/";
    vector<string> tokens;

    mrpt::system::tokenize	(sceneFileName,"/",tokens);

    for (size_t i_token = 0; i_token < tokens.size()-3; i_token++ )
        rawlogFileName.append(tokens[i_token]+"/");

    rawlogFileName.append("7 - Labeled RGBD data/");
    rawlogFileName.append(tokens[tokens.size()-2]+"/");
    rawlogFileName.append(tokens[tokens.size()-1].substr(0,tokens[tokens.size()-1].size()-5)+"rawlog");

    if (!mrpt::system::fileExists(rawlogFileName))
    {
        cerr << "  [ERROR] A rawlog file with name " << rawlogFileName;
        cerr << " doesn't exist." << endl;
        // return;
    }

    i_rawlog.open(rawlogFileName);

    cout << "  [INFO] Rawlog file   : " << rawlogFileName << endl;

    //
    // Process rawlog

    CActionCollectionPtr action;
    CSensoryFramePtr observations;
    CObservationPtr obs;
    size_t obsIndex = 0;
    size_t scanIndex = 0;

    cout.flush();

    map<string,TObsContent > m_lastObs;

    while ( CRawlog::getActionObservationPairOrObservation(i_rawlog,action,observations,obs,obsIndex) )
    {
        // Check that it is a 3D observation
        if ( !IS_CLASS(obs, CObservation3DRangeScan) )
            continue;

        CObservation3DRangeScanPtr obs3D = CObservation3DRangeScanPtr(obs);

        CObservation3DRangeScan::TPixelLabelInfoBase::TMapLabelID2Name &insertedLabels
                = obs3D->pixelLabels->pixelLabelNames;
        CObservation3DRangeScan::TPixelLabelInfoBase::TMapLabelID2Name::iterator it;

        vector<size_t> v_appearingObjects;

        for ( it = insertedLabels.begin(); it != insertedLabels.end(); it++ )
        {
            size_t objID = getObjectID(it->second,v_objects);

            for ( size_t i = 0; i < v_objects.size(); i++ )
            {
                TObject &obj = v_objects[i];
                if( obj.cloud->size() && !isnan(obj.planarity))
                    v_appearingObjects.push_back(objID);
            }
        }

        // CHECK IF THERE IS ANY OBJECT NEW OR REMOVED FROM THE LAST OBS OF THIS SENSOR

        bool insert = true;

        if ( m_lastObs.count(obs3D->sensorLabel) )  // First observation?
            // If they have different size, something happened :)
            if ( v_appearingObjects.size() == m_lastObs[obs3D->sensorLabel].objects.size() )
            {
                // Don't insert unless we find a different object
                insert = false;

                for ( size_t i_obj = 0; i_obj < v_appearingObjects.size(); i_obj ++)
                    if ( find(m_lastObs[obs3D->sensorLabel].objects.begin(),
                              m_lastObs[obs3D->sensorLabel].objects.end(),
                              v_appearingObjects[i_obj])
                         == m_lastObs[obs3D->sensorLabel].objects.end() ) // Different?
                    {
                        insert = true;
                        break;
                    }
            }


        if ( insert )
        {
            TObsContent obsContent;
            obsContent.sensorLabel = obs3D->sensorLabel;
            obsContent.ID = obsID++;

            if ( m_lastObs.count(obs3D->sensorLabel) ) // ? First observation
                characterizeObs(obsContent,
                                obs3D,
                                &(m_lastObs[obs3D->sensorLabel]));
            else
                characterizeObs(obsContent,
                                obs3D,
                                NULL);

            for ( size_t i = 0; i < v_appearingObjects.size(); i++ )
                obsContent.objects.push_back(v_appearingObjects[i]);

            // Find temporal closest scan
            bool found = false;

            do
            {
                if ( timeDifference(obs3D->timestamp,v_scans[scanIndex].time) > 0 )
                {
                    found = true;
                    obsContent.scan = v_scans[scanIndex];
                }
                else
                    scanIndex++;

            } while ((!found) && ( scanIndex < v_scans.size()));

            if (!found) // No more laser scans available, break the loop
                break;

            v_obsContent.push_back(obsContent);

            // Update las observation from this sensor
            m_lastObs[obs3D->sensorLabel] = obsContent;

            //            cout << "Added Sensor " << obs3D->sensorLabel;
            //            showVectorContent(" content ",obsContent.objects);
            //            cout << "Obs time : " << mrpt::system::timeToString(obs3D->timestamp) << endl;
            //            cout << "Scan time: " << mrpt::system::timeToString(obsContent.scan.time) << endl;
            //            mrpt::system::sleep(5000);

        }
        else
        {
            //            cout << "Skipping Sensor " << obs3D->sensorLabel;
            //            showVectorContent(" content ",v_appearingObjects);
        }
    }
}


//-----------------------------------------------------------
//					    storeData
//-----------------------------------------------------------

void storeData( const string &sceneFileName,
                vector<TObject> &v_objects,
                vector<TRelation> &v_relations,
                vector<TObsContent> &v_obsContent,
                size_t i_home, size_t i_roomType )
{
    cout << "[INFO] Storing data. Scene filename: " << sceneFileName << endl;
    ofstream    file;
    string      fileName;

    vector<string> tokens;

    mrpt::system::tokenize	(sceneFileName,"/",tokens);

    fileName.append("features_");
    fileName.append(tokens[tokens.size()-2]);
    fileName.append("_");
    fileName.append(tokens[tokens.size()-1].substr(0,tokens[tokens.size()-1].size()-15));
    fileName.append(".txt");
    cout << "Jir" << endl;

    cout << "  [INFO] Storing data in " << fileName << "... ";
    cout.flush();

    file.open( fileName.c_str() );

    if ( file.is_open() )
    {
        cout << " storing... " << fileName;

        // STORE SCENE INFO
        file << "Home " << v_homes[i_home] << " " << i_home
             << " Room_type " << v_typesOfRooms[i_roomType] << " " << i_roomType
             << " ID " << objectID++;

        // STORE OBJECTS
        //

        size_t N_validObjects = 0;
        for ( size_t i = 0; i < v_objects.size(); i++ )
            if ( v_objects[i].cloud->size() && !isNaN(v_objects[i].planarity) )
                N_validObjects++;

        file << " N_objects " << N_validObjects;
        file << " N_objectFeatures " << "32" << endl;

        //cout << " N_validObjects " << N_validObjects << endl;

        for ( size_t i_obj = 0; i_obj < v_objects.size(); i_obj++ )
        {
            TObject &obj = v_objects[i_obj];

            //cout << "    Storing " << obj.label << endl;

            if ( !obj.cloud->size() || isNaN(obj.planarity) )
                continue;

            file << obj.label << " " << obj.ID << " " << obj.type << " " << obj.gt << " ";
            file << obj.planarity << " " << obj.scatter << " " << obj.linearity << " ";
            file << obj.minHeight << " " << obj.maxHeight << " " << obj.centroid_x << " ";
            file << obj.centroid_y << " " << obj.centroid_z << " " << obj.volume << " ";
            file << obj.biggestArea << " " << obj.orientation << " " << obj.hueMean << " ";
            file << obj.satMean << " " << obj.valMean << " " << obj.hueStdv << " ";
            file << obj.satStdv << " " << obj.valStdv << " ";
            for ( size_t i = 0; i < 5; i++ ) file << obj.hue_hist[i] << " ";
            for ( size_t i = 0; i < 5; i++ ) file << obj.val_hist[i] << " ";
            for ( size_t i = 0; i < 5; i++ ) file << obj.sat_hist[i] << " ";
            file << endl;
        }

        // STORE RELATIONS
        //

        //        cout << "    Storing relations." << endl;
        //        cout << "N_relations" << v_relations.size();
        //        cout.flush();

        file << "N_relations " << v_relations.size();

        file << " N_relationFeatures " << v_relations[0].features.size() << endl;

        for ( size_t i_rel = 0; i_rel < v_relations.size(); i_rel++ )
        {
            TRelation &rel = v_relations[i_rel];

            //cout << "    Storing relation " << rel.relationID << endl;

            file << rel.label1 << " " << rel.label2 << " "
                 << rel.relationID << " "
                 << rel.ID1 << " " << rel.ID2 << " "
                 << rel.gt1 << " " << rel.gt2 << " ";

            for ( size_t i_feat = 0; i_feat < rel.features.size(); i_feat++ )
                file << rel.features[i_feat] << " ";

            file << endl;
        }

        // STORE OBSERVATIONS
        //

        //cout << "    Storing observations." << endl;

        file << "N_observations " << v_obsContent.size();
        file << " N_roomFeatures " << v_obsContent[0].roomFeatures.size()*2;
        file << " N_scanFeatures " << v_obsContent[0].scan.scanFeatures.size() << endl;

        for ( size_t i_obs = 0; i_obs < v_obsContent.size(); i_obs++ )
        {
            TObsContent &obs = v_obsContent[i_obs];

            file << obs.sensorLabel << " ";
            file << obs.ID << " ";
            file << obs.objects.size() << " ";

            for ( size_t i_obj = 0; i_obj < obs.objects.size(); i_obj++ )
                file << obs.objects[i_obj] << " ";

            // TODO: CHECK IF THESE (ROOM) FEATURES CAN BE ACCUMULATED SOMEHOW

            for ( size_t i_roomFeat = 0; i_roomFeat < obs.roomFeatures.size(); i_roomFeat++ )
                file << obs.roomFeatures[i_roomFeat] << " ";

            for ( size_t i_roomFeat = 0; i_roomFeat < obs.meanRoomFeatures.size(); i_roomFeat++ )
                file << obs.meanRoomFeatures[i_roomFeat] << " ";

            for ( size_t i_scanFeat = 0; i_scanFeat < obs.scan.scanFeatures.size(); i_scanFeat++ )
                file << obs.scan.scanFeatures[i_scanFeat] << " ";

            file << endl;
        }

        cout << "Done!" << endl;

        file.close();
    }
    else
    {
        cerr << "  [ERROR] Opening file to store the information" << endl;
    }
}

//-----------------------------------------------------------
//                      storeTypes
//-----------------------------------------------------------

void storeTypes()
{
    cout << "N_homes " << v_homes.size() << endl;
    for ( size_t i_home = 0; i_home < v_homes.size(); i_home++ )
        cout << i_home << "\t" << v_homes[i_home] << endl;

    cout << "N_typesOfRooms " << v_typesOfRooms.size() << endl;
    for ( size_t i_room = 0; i_room < v_typesOfRooms.size(); i_room++ )
        cout << i_room << "\t" << v_typesOfRooms[i_room] << endl;

    cout << "N_typesOfObjects " << v_objectTypes.size() << endl;
    for ( size_t i_obj = 0; i_obj < v_objectTypes.size(); i_obj++ )
        cout << i_obj << "\t" << v_objectTypes[i_obj] << endl;

    cout << "Frequency of objects: " << endl;
    map<string,size_t>::iterator it;

    for ( it = m_objectTypes.begin(); it != m_objectTypes.end(); it++ )
        cout << it->first << "\t" << it->second << endl;
}

//-----------------------------------------------------------
//							main
//-----------------------------------------------------------

int main()
{
    // Homes
    v_homes.push_back("alma-s1");
    v_homes.push_back("anto-s1");
    v_homes.push_back("pare-s1");
    v_homes.push_back("rx2-s1");
    v_homes.push_back("sarmis-s1");
    v_homes.push_back("sarmis-s2");
    v_homes.push_back("sarmis-s3");

    // Types of rooms
    v_typesOfRooms.push_back("bathroom");
    v_typesOfRooms.push_back("bedroom");
    v_typesOfRooms.push_back("corridor");
    //v_typesOfRooms.push_back("fullhouse");
    //v_typesOfRooms.push_back("hall");
    v_typesOfRooms.push_back("kitchen");
    v_typesOfRooms.push_back("livingroom");
    v_typesOfRooms.push_back("masterroom");
    //v_typesOfRooms.push_back("livingroomkitchen");

    // Transformation matrix from MRPT to PCL coordinates
    transMat(0,0)=0;    transMat(0,1)=-1;     transMat(0,2)=0;    transMat(0,3)=0;
    transMat(1,0)=0;    transMat(1,1)=0;      transMat(1,2)=+1;   transMat(1,3)=0;
    transMat(2,0)=1;    transMat(2,1)=0;      transMat(2,2)=0;    transMat(2,3)=0;
    transMat(3,0)=0;    transMat(3,1)=0;      transMat(3,2)=0;    transMat(3,3)=1;

    // VISUALIZER

    viewer->initCameraParameters ();
    viewer->addCoordinateSystem (1.0);


    // ITERATE OVER APARTMENTS
    //

    cout << "[INFO] Iterating over homes." << endl;

    for ( size_t h = 0; h < v_homes.size(); h++ )
    {
        // ITERATE OVER ROOMS
        //

        cout << "[INFO] Iterating over rooms in " << v_homes[h] << endl;

        for ( size_t r = 0; r < v_typesOfRooms.size(); r++ )
        {
            vector <string> v_scenesToProcess;
            getScenesToProcess(v_homes[h],v_typesOfRooms[r],v_scenesToProcess);

            for ( size_t s =0; s < v_scenesToProcess.size(); s++ )
            {
                cout << "[INFO] Processing scene: " << v_scenesToProcess[s] << endl;

                mrpt::opengl::COpenGLScenePtr scene = mrpt::opengl::COpenGLScene::Create();
                vector<TLabelledBox> v_labelled_boxes;
                vector<string>       v_appearingLabels;
                vector<TObject>      v_objects;

                // LOAD THE SCENE
                //

                loadLabelledScene(v_scenesToProcess[s],scene,v_labelled_boxes,v_appearingLabels);

                for ( size_t i = 0; i < v_labelled_boxes.size(); i++ )
                    cout  << "    " << v_labelled_boxes[i].label << endl;

                showVectorContent("Object types so far: ",v_objectTypes);

                if (scenePointCloud)
                    cout << "    Size of the point cloud: " << scenePointCloud->size() << endl;
                else
                    cout << " Not available point cloud" << endl;

                // CONVERT SCENE TO PCL FORMAT AND COORDINATES SYSTEM
                //

                pcl::PointCloud<pcl::PointXYZRGB>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZRGB>);
                pcl::PointCloud<pcl::PointXYZ>::Ptr auxCloud(new pcl::PointCloud<pcl::PointXYZ>());

                convertMRPTsceneToPCL(cloud,auxCloud);

                // EXTRACT OBJECTS FROM THE SCENE
                //

                //extractObjectsFromScene(v_labelled_boxes,v_objects,cloud,auxCloud);

                // CHARACTERIZE OBJECTS
                //

                cout << "[INFO] Characterizing objects ... ";
                cout.flush();

                for ( size_t i_obj = 0; i_obj < v_objects.size(); i_obj++ )
                {
                    TObject &obj1 = v_objects[i_obj];
                    //characterizeObject(obj1);
                }

                cout << "Done!" << endl;

                // CHARACTERIZE RELATIONS
                //

                vector<TRelation> v_relations;

                cout << "[INFO] Characterizing relations ... ";
                cout.flush();

                //characterizeRelations(v_objects,v_relations);

                cout << "Done!" << endl;

                /*for ( size_t i = 0; i < v_relations.size(); i++ )
                {
                    cout << v_relations[i].label1 << " " << v_relations[i].label2 << " ";
                    for ( size_t j = 0; j < v_relations[i].features.size(); j++ )
                        cout << v_relations[i].features[j] << " ";
                    cout << endl;
                }*/

                // ITERATE OVER THE ASSOCIATED RAWLOG
                //

                cout << "[INFO] Processing rawlog ... " << endl;
                cout.flush();

                vector<TObsContent> v_obsContent;
                //processRawlog(v_scenesToProcess[s],v_obsContent,v_objects);

                cout << "[INFO] Processing rawlog ... DONE!" << endl;

                // STORE ALL THE INFORMATION INTO A FILE
                //

//                storeData(v_scenesToProcess[s],
//                          v_objects,
//                          v_relations,
//                          v_obsContent,
//                          h, r);

                //mrpt::system::pause();
            }
        }

    }

    // STORE THE OBJECT AND ROOM TYPES
    // Employ v_objectTypes
    storeTypes();

    return 0;
}

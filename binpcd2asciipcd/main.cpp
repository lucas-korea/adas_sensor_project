#include "pclEnvironment.h"
#include "openCVEnviron.h"
#include "fileOpen.h"




struct CameraCalData
{
	cv::Mat extrinsic;
	cv::Mat intrinsic;
	cv::Mat distCoeff;
	cv::Size imgSize;
};

CameraCalData readCameraCalData(const std::string paramPath)
{
	CameraCalData calData;	

	calData.extrinsic = cv::Mat::zeros(4, 4, CV_64F);
	calData.intrinsic = cv::Mat::zeros(3, 3, CV_64F);
	calData.distCoeff = cv::Mat::zeros(1, 4, CV_64F);
	calData.imgSize = cv::Size(0, 0);

	FILE *fp;

	fp = fopen(paramPath.c_str(), "rt");
	if(!fp) return calData;

	fscanf(fp, "CameraExtrinsicMat: ");
	fscanf(fp, "rows: 4 ");
	fscanf(fp, "cols: 4 ");
	fscanf(fp, "dt: d ");
	fscanf(fp, "data: [ %lf, %lf, %lf, %lf, %lf, %lf, %lf, %lf, %lf, %lf, %lf, %lf, %lf, %lf, %lf, %lf] ",
		&calData.extrinsic.at<double>(0, 0), &calData.extrinsic.at<double>(0, 1), &calData.extrinsic.at<double>(0, 2), &calData.extrinsic.at<double>(0, 3),
		&calData.extrinsic.at<double>(1, 0), &calData.extrinsic.at<double>(1, 1), &calData.extrinsic.at<double>(1, 2), &calData.extrinsic.at<double>(1, 3),
		&calData.extrinsic.at<double>(2, 0), &calData.extrinsic.at<double>(2, 1), &calData.extrinsic.at<double>(2, 2), &calData.extrinsic.at<double>(2, 3),
		&calData.extrinsic.at<double>(3, 0), &calData.extrinsic.at<double>(3, 1), &calData.extrinsic.at<double>(3, 2), &calData.extrinsic.at<double>(3, 3));

	fscanf(fp, "CameraMat: ");
	fscanf(fp, "rows: 3 ");
	fscanf(fp, "cols: 3 ");
	fscanf(fp, "dt: d ");
	fscanf(fp, "data: [ %lf, %lf, %lf, %lf, %lf, %lf, %lf, %lf, %lf] ",
		&calData.intrinsic.at<double>(0, 0), &calData.intrinsic.at<double>(0, 1), &calData.intrinsic.at<double>(0, 2), 
		&calData.intrinsic.at<double>(1, 0), &calData.intrinsic.at<double>(1, 1), &calData.intrinsic.at<double>(1, 2), 
		&calData.intrinsic.at<double>(2, 0), &calData.intrinsic.at<double>(2, 1), &calData.intrinsic.at<double>(2, 2));

	fscanf(fp, "DistCoeff: ");
	fscanf(fp, "rows: 1 ");
	fscanf(fp, "cols: 4 ");
	fscanf(fp, "dt: d ");
	fscanf(fp, "data: [ %lf, %lf, %lf, %lf] ",
		&calData.distCoeff.at<double>(0, 0), &calData.distCoeff.at<double>(0, 1), &calData.distCoeff.at<double>(0, 2), &calData.distCoeff.at<double>(0, 3));

	fscanf(fp, "ImageSize: [ %d, %d ]", &calData.imgSize.height, &calData.imgSize.width);
	fclose(fp);

	return calData;
}

cv::Scalar convertDist2Color(double dist)
{
	cv::Scalar color = cv::Scalar(0, 0, 0);

	if(dist!=0)
	{
		if(dist < 255)
		{
			color[0] = dist;
		}			
		else if(dist < 510)
		{
			color[0] = MAX(MIN(510 - dist, 255), 0);
			color[1] = MAX(MIN(dist - 255, 255), 0);
		}
		else
		{
			color[1] = MAX(MIN(765 - dist, 255), 0);
			color[2] = MAX(MIN(dist - 510, 255), 0);
		}

	}	

	return color;
}

void main()
{
	std::string imgFilePath = "C:/Users/sky/Desktop/lidar-camera/2_20210713_113924_000120_27.png";
	std::string lidarFilePath = "C:/Users/sky/Desktop/lidar-camera/2_20210713_113924_000120_27.pcd";
	std::string calDataPath = "C:/Users/sky/Desktop/lidar-camera/cam-lidarCalibration.yml";

	imgFilePath = openfilename(NULL, "All Img Files(*.png)\0 *.png\0");	
	lidarFilePath = openfilename(NULL, "All LiDAR Files(*.pcd)\0 *.pcd\0");	
	calDataPath = openfilename(NULL, "All Camera-LiDAR Files(*.yml)\0 *.yml\0");	

	//cal param read
	CameraCalData calData = readCameraCalData(calDataPath);
	std::cout << calData.extrinsic << std::endl;
	std::cout << calData.intrinsic << std::endl;
	std::cout << calData.distCoeff << std::endl;

	//pcd read
	pcl::PointCloud<pcl::PointXYZ>::Ptr cloud (new pcl::PointCloud<pcl::PointXYZ>);
	if (pcl::io::loadPCDFile<pcl::PointXYZ> (lidarFilePath, *cloud) == -1) //* load the file
	{
		PCL_ERROR ("Couldn't read file /n");
		return;
	}

	std::cout<<"Loaded" << 
		cloud->width * cloud->height <<
		"data points from filename with the following fields: " << std::endl;
	
	//transform matrix
	cv::Mat rotation = calData.extrinsic(cv::Rect(0, 0, 3, 3));
	cv::Mat translation = calData.extrinsic(cv::Rect(3, 0, 1, 3));
	rotation = rotation.t();
	translation = -rotation * translation;

	std::vector<cv::Point3f> pointCloudPos;
	for(size_t i = 0; i < cloud->points.size(); ++i)
	{
		if(fabs(cloud->points[i].x) < 0.01 && fabs(cloud->points[i].y) < 0.01 && fabs(cloud->points[i].z) < 0.01)
			continue;

		cv::Mat lidarPoint = (cv::Mat_<double>(3, 1) << cloud->points[i].x, cloud->points[i].y, cloud->points[i].z);
		cv::Mat transPoint = rotation * lidarPoint + translation;

		if(transPoint.at<double>(2) < 0)  //영상 뒤쪽으로 가는 포인트는 제거
			continue;

		cv::Point3f lidarPos = cv::Point3f(cloud->points[i].x, cloud->points[i].y, cloud->points[i].z );
		pointCloudPos.push_back(lidarPos);
	}

	std::vector<cv::Point2f> projectedPos;
	cv::projectPoints(pointCloudPos, rotation, translation, calData.intrinsic, calData.distCoeff, projectedPos);

	//img read
	cv::Mat img = cv::imread(imgFilePath);

	//lidar map
	cv::Mat lidarMap = cv::Mat::zeros(1000, 1000, CV_8UC3);

	//point display
	for(size_t i = 0; i < pointCloudPos.size(); ++i)
	{
		cv::Point3f lidarPt = pointCloudPos.at(i);
		cv::Point2f projectedPt = projectedPos.at(i);

		//영상을 벗어난 좌표체크
		if(	projectedPt.x >= 0 && projectedPt.x < img.cols &&
			projectedPt.y >= 0 && projectedPt.y < img.rows)
		{
			//카메라 좌표계로 변환
			cv::Mat lidarPoint = (cv::Mat_<double>(3, 1) << lidarPt.x, lidarPt.y, lidarPt.z);
			cv::Mat transPoint = rotation * lidarPoint + translation;
			
			//거리값을 컬러로 표현
			double dist = transPoint.at<double>(2) * 50;
			cv::Scalar color = convertDist2Color(dist);
			
			//해당 위치에 표시
			cv::circle(img, cv::Point(projectedPt.x, projectedPt.y), 1, color, 3);
			cv::circle(lidarMap, cv::Point(transPoint.at<double>(0) * 100 + lidarMap.cols/2, transPoint.at<double>(1) * 100 + lidarMap.rows/2), 2, color);
		}
	}

	cv::resize(img, img, cv::Size(img.cols/2, img.rows/2)) ;
	cv::imshow("img", img);
	cv::imshow("lidar", lidarMap);


	////undistortion
	//cv::Mat undistortImg;
	//cv::undistort(img, undistortImg, calData.intrinsic, calData.distCoeff);
	//cv::imshow("undistortImg", undistortImg);

	

	cv::waitKey();


}
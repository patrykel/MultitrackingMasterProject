

/****************************************************************************
 *
 * This is a part of TOTEM offline software.
 * Authors:
 *   Patryk Ławski (patryk.jakub.lawski@cern.ch, patryk.lawski@gmail.com)
 *
 ****************************************************************************/



#ifndef DemoAnalyzer_GeometryUtility
#define DemoAnalyzer_GeometryUtility

#include "RecoTotemRP/RPRecoDataFormats/interface/RPRecognizedPatterns.h"
#include "DataFormats/TotemRPDataTypes/interface/RPRecoHit.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include <iostream>
#include <sstream>

#include "TTree.h"
#include "TFile.h"
#include "TSystemDirectory.h"

class GeometryUtility {

  public:

    explicit GeometryUtility();
    ~GeometryUtility();

    static const unsigned int arm_number = 2;
    static const unsigned int station_per_arm = 2;
    static const unsigned int rp_per_station = 6;
    static const unsigned int silicons_per_rp = 10;

    
    struct PossibleHitPoint{
      double x;   // [mm] global coordinate
      double y;   // [mm] global coordinate
      double z;   // [mm] global coordinate
    };

    struct Point{
      double x;   
      double y;   
      double z;
    };

    struct Direction{
      double dx;
      double dy;
    };

    struct Vector2D{
      double x;
      double y;
    };


    // Point getCenter(RPRecoHit recoHit);
    // Direction getReadoutDirection(RPRecoHit recoHit);
    // Direction getPerpendicularDirection(GeometryUtility::Direction direction);


    // ROOT FILE RELATED
    void prepareRootFile();
    void closeRootFile();
    void exportGeometryToRoot();
    TFile *f;
    TTree *T;
    Int_t detIdRoot;
    Float_t xRoot, yRoot, zRoot, dxRoot, dyRoot;

    void printGeometryUtilityData();
    PossibleHitPoint getIntersection(RPRecoHit uHit, RPRecoHit vHit);

    void getPossibleHitPoints(std::vector<RPRecognizedPatterns::Line> uLines, 
      std::vector<RPRecognizedPatterns::Line> vLines,
      unsigned int uSiliconNo,
      unsigned int vSiliconNo,
      std::vector<GeometryUtility::PossibleHitPoint> &possibleHits, 
      std::ostringstream &oss);

    void getPossibleHitPoint(RPRecognizedPatterns::Line uLine, 
      RPRecognizedPatterns::Line vLine, 
      std::vector<GeometryUtility::PossibleHitPoint> &possibleHits, 
      std::ostringstream &oss);

    double getX(int armId, int stationId, int rpId, int siliconId);
    double getY(int armId, int stationId, int rpId, int siliconId);
    double getZ(int armId, int stationId, int rpId, int siliconId);
    double getDx(int armId, int stationId, int rpId, int siliconId);
    double getDy(int armId, int stationId, int rpId, int siliconId);

// private:

    int getIdx(int armId, int stationId, int rpId, int siliconId);
    GeometryUtility::Point getCenter(RPRecoHit recoHit);
    GeometryUtility::Direction getReadoutDirection(RPRecoHit recoHit);
    GeometryUtility::Direction getPerpendicularDirection(GeometryUtility::Direction direction);

    double x[240] = {-0.514, 0.514, -0.514, 0.514, -0.514, 0.514, -0.514, 0.514, -0.514, 0.514, 0.514, -0.514, 0.514,
                  -0.514, 0.514, -0.514, 0.514, -0.514, 0.514, -0.514, 57.140, 57.140, 57.140, 57.140, 57.140, 57.140,
                  57.140, 57.140, 57.140, 57.140, 21.570, 21.741, 21.583, 21.755, 21.637, 21.755, 21.627, 21.771,
                  21.685, 21.795, -3.521, -2.470, -3.481, -2.449, -3.446, -2.424, -3.401, -2.402, -3.386, -2.400, 3.513,
                  2.612, 3.551, 2.586, 3.579, 2.572, 3.594, 2.529, 3.654, 2.509, -1.175, 0.014, -1.118, -0.030, -1.074,
                  -0.038, -1.010, -0.073, -0.940, -0.055, 0.163, -0.788, 0.165, -0.832, 0.166, -0.887, 0.177, -0.925,
                  0.126, -0.975, 21.638, 21.672, 21.670, 21.696, 21.694, 21.685, 21.721, 21.707, 21.748, 21.713, 21.159,
                  21.098, 21.178, 21.172, 21.202, 21.222, 21.262, 21.277, 21.286, 21.322, -0.687, 0.486, -0.650, 0.435,
                  -0.637, 0.371, -0.607, 0.380, -0.575, 0.310, 0.630, -0.249, 0.637, -0.325, 0.639, -0.405, 0.616,
                  -0.459, 0.664, -0.516, 0.514, -0.514, 0.514, -0.514, 0.514, -0.514, 0.514, -0.514, 0.514, -0.514,
                  -0.514, 0.514, -0.514, 0.514, -0.514, 0.514, -0.514, 0.514, -0.514, 0.514, 57.129, 57.129, 57.129,
                  57.129, 57.129, 57.129, 57.129, 57.129, 57.129, 57.129, 21.933, 21.936, 21.969, 21.891, 21.986,
                  21.845, 22.002, 21.793, 22.045, 21.755, -2.387, -3.403, -2.418, -3.410, -2.405, -3.425, -2.402,
                  -3.428, -2.418, -3.453, 2.707, 3.727, 2.722, 3.741, 2.713, 3.735, 2.690, 3.708, 2.661, 3.670, 1.043,
                  0.186, 1.110, 0.160, 1.156, 0.137, 1.223, 0.089, 1.263, 0.093, -0.663, 0.481, -0.652, 0.444, -0.607,
                  0.428, -0.589, 0.361, -0.570, 0.344, 21.810, 21.833, 21.808, 21.828, 21.780, 21.776, 21.762, 21.746,
                  21.750, 21.726, 21.072, 21.122, 21.088, 21.085, 21.087, 21.065, 21.066, 21.041, 21.037, 21.038,
                  -0.076, -1.063, -0.058, -1.056, -0.048, -1.054, -0.020, -1.092, -0.010, -1.086, -1.269, -0.165,
                  -1.248, -0.183, -1.204, -0.190, -1.210, -0.220, -1.194, -0.229};

    double y[240] = {56.004, 56.004, 56.004, 56.004, 56.004, 56.004, 56.004, 56.004, 56.004, 56.004, -56.353, -56.353,
                  -56.353, -56.353, -56.353, -56.353, -56.353, -56.353, -56.353, -56.353, 0.514, -0.514, 0.514, -0.514,
                  0.514, -0.514, 0.514, -0.514, 0.514, -0.514, 3.945, 2.860, 3.935, 2.877, 3.893, 2.877, 3.901, 2.898,
                  3.857, 2.929, 19.604, 19.878, 19.657, 19.862, 19.704, 19.843, 19.764, 19.827, 19.783, 19.825, -20.145,
                  -20.239, -20.094, -20.219, -20.056, -20.208, -20.036, -20.176, -19.957, -20.161, 20.216, 20.279,
                  20.273, 20.323, 20.318, 20.331, 20.381, 20.365, 20.452, 20.347, -20.594, -20.678, -20.593, -20.634,
                  -20.591, -20.579, -20.580, -20.542, -20.631, -20.491, 1.671, 0.564, 1.639, 0.587, 1.614, 0.577, 1.586,
                  0.598, 1.559, 0.604, 0.800, -0.405, 0.781, -0.331, 0.757, -0.281, 0.696, -0.227, 0.672, -0.182,
                  20.720, 20.686, 20.757, 20.737, 20.770, 20.801, 20.801, 20.792, 20.832, 20.862, -21.133, -21.267,
                  -21.126, -21.192, -21.123, -21.111, -21.147, -21.057, -21.098, -21.000, 56.012, 56.012, 56.012,
                  56.012, 56.012, 56.012, 56.012, 56.012, 56.012, 56.012, -56.059, -56.059, -56.059, -56.059, -56.059,
                  -56.059, -56.059, -56.059, -56.059, -56.059, -0.514, 0.514, -0.514, 0.514, -0.514, 0.514, -0.514,
                  0.514, -0.514, 0.514, 2.964, 3.983, 3.011, 4.017, 3.034, 4.052, 3.054, 4.091, 3.111, 4.120, 20.098,
                  19.997, 20.122, 19.988, 20.112, 19.968, 20.110, 19.965, 20.122, 19.931, -20.122, -19.958, -20.133,
                  -19.939, -20.126, -19.947, -20.109, -19.983, -20.087, -20.033, 22.143, 22.086, 22.079, 22.058, 22.035,
                  22.035, 21.970, 21.984, 21.932, 21.988, -20.523, -20.502, -20.535, -20.539, -20.580, -20.555, -20.598,
                  -20.622, -20.617, -20.639, 0.648, 1.596, 0.646, 1.602, 0.618, 1.654, 0.601, 1.684, 0.588, 1.704,
                  -0.445, 0.528, -0.429, 0.565, -0.431, 0.585, -0.451, 0.610, -0.480, 0.613, 21.043, 21.017, 21.025,
                  21.024, 21.016, 21.027, 20.988, 20.988, 20.978, 20.994, -21.153, -21.163, -21.173, -21.182, -21.217,
                  -21.188, -21.211, -21.219, -21.227, -21.228};

    double z[240] = {-203.3567, -203.3613, -203.3657, -203.3703, -203.3747, -203.3793, -203.3837, -203.3883, -203.3927,
                  -203.3973, -203.3567, -203.3613, -203.3657, -203.3703, -203.3747, -203.3793, -203.3837, -203.3883,
                  -203.3927, -203.3973, -203.8067, -203.8113, -203.8157, -203.8203, -203.8247, -203.8293, -203.8337,
                  -203.8383, -203.8427, -203.8473, -212.5297, -212.5343, -212.5387, -212.5433, -212.5477, -212.5523,
                  -212.5567, -212.5613, -212.5657, -212.5703, -212.9797, -212.9843, -212.9887, -212.9933, -212.9977,
                  -213.0023, -213.0067, -213.0113, -213.0157, -213.0203, -212.9797, -212.9843, -212.9887, -212.9933,
                  -212.9977, -213.0023, -213.0067, -213.0113, -213.0157, -213.0203, -214.6077, -214.6123, -214.6167,
                  -214.6213, -214.6257, -214.6303, -214.6347, -214.6393, -214.6437, -214.6483, -214.6077, -214.6123,
                  -214.6167, -214.6213, -214.6257, -214.6303, -214.6347, -214.6393, -214.6437, -214.6483, -215.0577,
                  -215.0623, -215.0667, -215.0713, -215.0757, -215.0803, -215.0847, -215.0893, -215.0937, -215.0983,
                  -219.5297, -219.5343, -219.5387, -219.5433, -219.5477, -219.5523, -219.5567, -219.5613, -219.5657,
                  -219.5703, -219.9797, -219.9843, -219.9887, -219.9933, -219.9977, -220.0023, -220.0067, -220.0113,
                  -220.0157, -220.0203, -219.9797, -219.9843, -219.9887, -219.9933, -219.9977, -220.0023, -220.0067,
                  -220.0113, -220.0157, -220.0203, 203.3567, 203.3613, 203.3657, 203.3703, 203.3747, 203.3793, 203.3837,
                  203.3883, 203.3927, 203.3973, 203.3567, 203.3613, 203.3657, 203.3703, 203.3747, 203.3793, 203.3837,
                  203.3883, 203.3927, 203.3973, 203.8067, 203.8113, 203.8157, 203.8203, 203.8247, 203.8293, 203.8337,
                  203.8383, 203.8427, 203.8473, 212.5297, 212.5343, 212.5387, 212.5433, 212.5477, 212.5523, 212.5567,
                  212.5613, 212.5657, 212.5703, 212.9797, 212.9843, 212.9887, 212.9933, 212.9977, 213.0023, 213.0067,
                  213.0113, 213.0157, 213.0203, 212.9797, 212.9843, 212.9887, 212.9933, 212.9977, 213.0023, 213.0067,
                  213.0113, 213.0157, 213.0203, 214.6077, 214.6123, 214.6167, 214.6213, 214.6257, 214.6303, 214.6347,
                  214.6393, 214.6437, 214.6483, 214.6077, 214.6123, 214.6167, 214.6213, 214.6257, 214.6303, 214.6347,
                  214.6393, 214.6437, 214.6483, 215.0577, 215.0623, 215.0667, 215.0713, 215.0757, 215.0803, 215.0847,
                  215.0893, 215.0937, 215.0983, 219.5297, 219.5343, 219.5387, 219.5433, 219.5477, 219.5523, 219.5567,
                  219.5613, 219.5657, 219.5703, 219.9797, 219.9843, 219.9887, 219.9933, 219.9977, 220.0023, 220.0067,
                  220.0113, 220.0157, 220.0203, 219.9797, 219.9843, 219.9887, 219.9933, 219.9977, 220.0023, 220.0067,
                  220.0113, 220.0157, 220.0203};

    double dx[240] = {0.707, -0.707, 0.707, -0.707, 0.707, -0.707, 0.707, -0.707, 0.707, -0.707, -0.707, 0.707, -0.707,
                   0.707, -0.707, 0.707, -0.707, 0.707, -0.707, 0.707, 0.707, 0.707, 0.707, 0.707, 0.707, 0.707, 0.707,
                   0.707, 0.707, 0.707, 0.795, 0.606, 0.795, 0.606, 0.795, 0.606, 0.795, 0.606, 0.795, 0.607, 0.601,
                   -0.798, 0.603, -0.798, 0.603, -0.798, 0.603, -0.798, 0.603, -0.798, -0.600, 0.800, -0.601, 0.800,
                   -0.602, 0.799, -0.601, 0.799, -0.602, 0.798, 0.707, -0.707, 0.707, -0.707, 0.707, -0.707, 0.707,
                   -0.707, 0.708, -0.707, -0.706, 0.708, -0.706, 0.707, -0.707, 0.708, -0.707, 0.707, -0.707, 0.708,
                   0.702, 0.712, 0.701, 0.712, 0.702, 0.713, 0.702, 0.712, 0.702, 0.712, 0.706, 0.709, 0.705, 0.708,
                   0.706, 0.709, 0.706, 0.709, 0.706, 0.708, 0.707, -0.707, 0.707, -0.707, 0.707, -0.707, 0.708, -0.707,
                   0.707, -0.706, -0.707, 0.707, -0.707, 0.707, -0.707, 0.707, -0.707, 0.707, -0.707, 0.707, -0.707,
                   0.707, -0.707, 0.707, -0.707, 0.707, -0.707, 0.707, -0.707, 0.707, 0.707, -0.707, 0.707, -0.707,
                   0.707, -0.707, 0.707, -0.707, 0.707, -0.707, 0.707, 0.707, 0.707, 0.707, 0.707, 0.707, 0.707, 0.707,
                   0.707, 0.707, 0.605, 0.796, 0.605, 0.796, 0.605, 0.796, 0.604, 0.797, 0.604, 0.797, -0.798, 0.602,
                   -0.798, 0.602, -0.798, 0.602, -0.799, 0.602, -0.799, 0.602, 0.799, -0.601, 0.798, -0.602, 0.799,
                   -0.602, 0.799, -0.602, 0.799, -0.602, -0.720, 0.693, -0.721, 0.693, -0.721, 0.693, -0.721, 0.694,
                   -0.721, 0.693, 0.706, -0.708, 0.706, -0.708, 0.707, -0.709, 0.706, -0.707, 0.706, -0.708, 0.710,
                   0.703, 0.710, 0.704, 0.711, 0.703, 0.711, 0.704, 0.711, 0.704, 0.710, 0.704, 0.710, 0.704, 0.710,
                   0.704, 0.710, 0.704, 0.710, 0.704, -0.706, 0.708, -0.706, 0.708, -0.707, 0.707, -0.707, 0.708,
                   -0.707, 0.707, 0.707, -0.707, 0.708, -0.706, 0.708, -0.706, 0.709, -0.705, 0.709, -0.705};

    double dy[240] = {0.707, 0.707, 0.707, 0.707, 0.707, 0.707, 0.707, 0.707, 0.707, 0.707, -0.707, -0.707, -0.707, -0.707,
                   -0.707, -0.707, -0.707, -0.707, -0.707, -0.707, -0.707, 0.707, -0.707, 0.707, -0.707, 0.707, -0.707,
                   0.707, -0.707, 0.707, -0.606, 0.795, -0.606, 0.795, -0.606, 0.795, -0.607, 0.795, -0.607, 0.795,
                   0.799, 0.603, 0.798, 0.603, 0.798, 0.603, 0.798, 0.602, 0.797, 0.603, -0.800, -0.600, -0.800, -0.601,
                   -0.799, -0.601, -0.799, -0.602, -0.799, -0.602, 0.708, 0.707, 0.708, 0.707, 0.707, 0.707, 0.707,
                   0.708, 0.707, 0.707, -0.708, -0.706, -0.708, -0.707, -0.708, -0.707, -0.707, -0.707, -0.707, -0.706,
                   -0.712, 0.702, -0.713, 0.702, -0.712, 0.701, -0.712, 0.702, -0.712, 0.702, -0.709, 0.706, -0.709,
                   0.706, -0.709, 0.705, -0.708, 0.706, -0.708, 0.706, 0.707, 0.707, 0.707, 0.707, 0.707, 0.707, 0.707,
                   0.707, 0.707, 0.708, -0.707, -0.707, -0.707, -0.707, -0.707, -0.707, -0.707, -0.707, -0.707, -0.707,
                   0.707, 0.707, 0.707, 0.707, 0.707, 0.707, 0.707, 0.707, 0.707, 0.707, -0.707, -0.707, -0.707, -0.707,
                   -0.707, -0.707, -0.707, -0.707, -0.707, -0.707, 0.707, -0.707, 0.707, -0.707, 0.707, -0.707, 0.707,
                   -0.707, 0.707, -0.707, 0.796, -0.605, 0.796, -0.605, 0.797, -0.605, 0.797, -0.604, 0.797, -0.604,
                   0.602, 0.798, 0.603, 0.798, 0.603, 0.798, 0.602, 0.799, 0.601, 0.798, -0.602, -0.799, -0.602, -0.798,
                   -0.602, -0.799, -0.602, -0.799, -0.602, -0.799, 0.693, 0.721, 0.693, 0.721, 0.693, 0.721, 0.693,
                   0.720, 0.693, 0.721, -0.708, -0.706, -0.708, -0.706, -0.707, -0.706, -0.708, -0.707, -0.708, -0.706,
                   0.704, -0.711, 0.704, -0.710, 0.703, -0.711, 0.704, -0.711, 0.704, -0.710, 0.704, -0.710, 0.704,
                   -0.711, 0.704, -0.710, 0.704, -0.710, 0.705, -0.710, 0.708, 0.706, 0.709, 0.706, 0.707, 0.707, 0.707,
                   0.707, 0.707, 0.707, -0.707, -0.708, -0.706, -0.708, -0.706, -0.708, -0.706, -0.709, -0.705, -0.709};
};


#endif 
// DemoAnalyzer_GeometryUtility
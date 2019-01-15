

/****************************************************************************
 *
 * This is a part of TOTEM offline software.
 * Authors:
 *   Patryk Ławski (patryk.jakub.lawski@cern.ch, patryk.lawski@gmail.com)
 *
 ****************************************************************************/

#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "RecoTotemRP/RPRecoDataFormats/interface/RPRecognizedPatternsCollection.h"
#include "RecoTotemRP/RPRecoDataFormats/interface/RPRecognizedPatterns.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/TotemRPDataTypes/interface/RPRecoHit.h"
#include "Demo/DemoAnalyzer/interface/GeometryUtility.h"
#include <memory>
#include <vector>
#include <fstream>
#include <sstream>
#include <string>
#include <iostream>
#include <stdio.h>



struct CombinedBinaryRecord {
   // DATA FIELDS
   int eventID;      // 4
   short recoId;     // 2
   char armID;       // 1
   char groupID;     // 1 --> 8
   char rpID;        // 1
   char uLineSize;   // 1
   char vLineSize;   // 1
   char siliconID;   // 1
   char direction;   // 1
   char line_no;     // 1 --> 6
   double position;  // 8
   // double sigma;
   double line_a;    // 8
   double line_b;    // 8
   double line_w;    // 8

   // CONSTRUCTOR
   CombinedBinaryRecord(int _eventID, short _recoId, char _armID, char _groupID, char _rpID, 
      char _uLineSize, char _vLineSize, short _siliconID, char _direction, char _line_no, double _position, 
      // double _sigma, 
      double _line_a, double _line_b, double _line_w) :           
     eventID(_eventID), recoId(_recoId), armID(_armID), groupID(_groupID), rpID(_rpID), uLineSize(_uLineSize), 
     vLineSize(_vLineSize), siliconID(_siliconID), direction(_direction), line_no(_line_no), position(_position), 
     // sigma(_sigma), 
     line_a(_line_a), line_b(_line_b), line_w(_line_w) {}
};


std::ostream& operator<<(std::ostream& stream, CombinedBinaryRecord const& data)
{
   stream << data.recoId
      << data.eventID            
      << data.armID
      << data.groupID
      << data.rpID
      << data.uLineSize
      << data.vLineSize
      << data.siliconID
      << data.direction  
      << data.line_no
      << data.position
      // << data.sigma
      << data.line_a
      << data.line_b
      << data.line_w;

    return stream;
}



class RecoBinaryCombinedSingleMulti : public edm::EDAnalyzer {
   public:
      explicit RecoBinaryCombinedSingleMulti(const edm::ParameterSet&);
      ~RecoBinaryCombinedSingleMulti();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);   // method fills 'descriptions' with the allowed parameters for the module
      
   private:
      virtual void beginJob() override;                                             // method called once each job just before starting event loop
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;     // method called for each event
      virtual void endJob() override;                                               // method called once each job just after ending the event loop
      
      //virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;    // method called when starting to processes a run
      //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;      // method called when ending the processing of a run
      //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;    // method called when starting to processes a luminosity block
      //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;      // method called when ending the processing of a luminosity block

      void hits_log(int eventID, char direction, unsigned int uLineSize, unsigned int vLineSize, RPRecognizedPatterns::Line &line, unsigned int line_no);
      void lines_log(std::vector<RPRecognizedPatterns::Line> &lines, char direction, int eventId, unsigned int uLinesNumber, unsigned int vLinesNumber);

      int lastEventId;
      int records_counter;
      std::vector<CombinedBinaryRecord> records;

      unsigned int row_counter;
      std::string fillFileName;
      fstream binary_file;
      unsigned int recoId; // first field of struct, provided in parameters
};

unsigned int getCombinedBinaryGroupId(unsigned int rawDetId);
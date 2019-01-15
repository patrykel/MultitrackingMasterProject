

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

class RecoCSVCombinedSingleMulti : public edm::EDAnalyzer {
   public:
      explicit RecoCSVCombinedSingleMulti(const edm::ParameterSet&);
      ~RecoCSVCombinedSingleMulti();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);   // method fills 'descriptions' with the allowed parameters for the module

      struct CombinedRecord {
         // DATA FIELDS
         std::string recoId;
         int eventID;
         unsigned int armID;
         unsigned int groupID;
         unsigned int rpID;
         unsigned int uLineSize;
         unsigned int vLineSize;
         unsigned int siliconID;
         std::string direction;
         unsigned int line_no;
         double position;
         double sigma;
         double line_a;
         double line_b;
         double line_w;

         // CONSTRUCTOR
         CombinedRecord(std::string _recoId, int _eventID, unsigned int _armID, unsigned int _groupID, unsigned int _rpID, 
            unsigned int _uLineSize, unsigned int _vLineSize, unsigned int _siliconID, std::string _direction, 
            unsigned int _line_no, double _position, double _sigma, double _line_a, double _line_b, double _line_w) :           
         
           recoId(_recoId), eventID(_eventID), armID(_armID), groupID(_groupID), rpID(_rpID), 
           uLineSize(_uLineSize), vLineSize(_vLineSize), siliconID(_siliconID), direction(_direction), 
           line_no(_line_no), position(_position), sigma(_sigma), line_a(_line_a), line_b(_line_b), line_w(_line_w) {}
      };


   private:
      virtual void beginJob() override;                                             // method called once each job just before starting event loop
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;     // method called for each event
      virtual void endJob() override;                                               // method called once each job just after ending the event loop
      
      //virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;    // method called when starting to processes a run
      //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;      // method called when ending the processing of a run
      //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;    // method called when starting to processes a luminosity block
      //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;      // method called when ending the processing of a luminosity block

      void hits_log(int eventID, std::string &direction, unsigned int uLineSize, unsigned int vLineSize, RPRecognizedPatterns::Line &line, unsigned int line_no);
      void lines_log(std::vector<RPRecognizedPatterns::Line> &lines, std::string &direction, int eventId, unsigned int uLinesNumber, unsigned int vLinesNumber);

      int records_counter;
      std::vector<CombinedRecord> records;

      unsigned int row_counter;
      std::string fillFileName;
      ofstream combinedCSV;  // to create csv file for dumping hit record (data useful for single and multitracking) 
      std::string recoId; // first field of CSV, provided in parameters
};

unsigned int getCombinedGroupId(unsigned int rawDetId);
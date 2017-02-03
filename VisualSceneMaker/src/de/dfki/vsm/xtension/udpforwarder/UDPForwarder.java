/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package de.dfki.vsm.xtension.udpforwarder;

import de.dfki.vsm.model.config.ConfigFeature;
import de.dfki.vsm.model.project.PluginConfig;
import de.dfki.vsm.model.scenescript.ActionFeature;
import de.dfki.vsm.runtime.activity.AbstractActivity;
import de.dfki.vsm.runtime.activity.ActionActivity;
import de.dfki.vsm.runtime.activity.SpeechActivity;
import de.dfki.vsm.runtime.activity.executor.ActivityExecutor;
import de.dfki.vsm.runtime.project.RunTimeProject;
import de.dfki.vsm.util.log.LOGConsoleLogger;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.InterfaceAddress;
import java.net.NetworkInterface;
import java.net.SocketException;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.LinkedList;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * This is an empty basic executor showing the basic needs and functionalities
 * of a VisualMaker extension;
 * useful start point to implement your own Device.
 *
 * @author Fabrizio Nunnari
 */
public class UDPForwarder extends ActivityExecutor {

    private static final String PREFIX = "------";

    /** The prefix used to identify ActionActivity blocks in sentences. */
    private static final String BLOCK_PREFIX = "\\UDPFwd=";

    private static final int UDP_BROADCAST_PORT = 23000;

    // The singleton logger instance
    private final LOGConsoleLogger mLogger = LOGConsoleLogger.getInstance();


    private DatagramSocket mDatagramSocket ;
    private LinkedList<InetAddress> mBroadcastAddresses = new LinkedList<InetAddress>();

    public UDPForwarder(PluginConfig config, RunTimeProject project) {
        super(config, project);
        ArrayList<ConfigFeature> configFeatures = mConfig.getEntryList();
//        mLogger.message("Found " + configFeatures.size() + " features:");
        for (ConfigFeature cf: configFeatures) {
//            mLogger.message(String.format(" - key=%s, name=%s, value=%s", cf.getKey(), cf.getName(), cf.getValue()));
        }

    }


    /** This serves to create a unique prefix for your blocks. */
    @Override
    public String marker(long id) {
        return BLOCK_PREFIX + id ;
    }


    /** This method is invoked every time a scene is played. */
    @Override
    public void execute(AbstractActivity activity) {

        //
        // General Activity information
        //
        String a_name = activity.getName();
        AbstractActivity.Type a_type = activity.getType();
        String a_actor = activity.getActor();
        String a_mode = activity.getMode();

//        mLogger.message(
//                    String.format("Got execute for action name=%s, type=%s, type=, actor=, mode=",
//                                a_name, a_type, a_actor, a_mode));

        LinkedList<ActionFeature> a_features = activity.getFeatures();
        if (a_features != null) {
//            mLogger.message("Festures ("+a_features.size()+")") ;
            for (ActionFeature af: a_features) {
                String af_key = af.getKey();
                ActionFeature.Type af_type = af.getTyp();
                String af_val = af.getVal();
                mLogger.message(String.format(" - key=%s, type=%s, val=%s", af_key, af_type, af_val));
            }
        } else {
            mLogger.message("No Features");
        }

        //
        // Now we distinguish between specific Activity subclasses
        //
        if (activity instanceof SpeechActivity) {
            SpeechActivity sa = (SpeechActivity) activity;

            String sa_textonly = sa.getTextOnly(BLOCK_PREFIX).trim();
            String sa_punct = sa.getPunct();

            // broadcast the text on the network.
//            broadcastMessage(sa_textonly);
            broadcastMessage(toJson(activity));

            //
            // The following lines of code will extract all the Action blocks
            // from the speech and forward them to the global scheduler in
            // order to trigger the execution of the ActionActivities.
            LinkedList<String> timemarks = sa.getTimeMarks(BLOCK_PREFIX);
            for (String tm : timemarks) {
                mProject.getRunTimePlayer().getActivityScheduler().handle(tm);
            }

        } else if (activity instanceof ActionActivity) {
            ActionActivity aa = (ActionActivity) activity;
            String aa_text = aa.getText();

            // broadcast the text on the network.
//            broadcastMessage(aa_text);
            broadcastMessage(toJson(activity));

        } else {
            mLogger.warning("Unhandled Activity subclass: " + activity.getClass().getName()) ;
        }

    }


    /** Convert the string into UTF8 bytes and broadcast the string to all
     * known broadcast addresses on this machine.
     */
    private void broadcastMessage(String message) {
        try {
            byte[] sendData = message.getBytes("UTF8");
            for (InetAddress bc_addr : mBroadcastAddresses) {

                DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, bc_addr, UDP_BROADCAST_PORT);
                try {
                    mDatagramSocket.send(sendPacket);
                    String msg = message + " sent to " + bc_addr.getHostAddress() + " length: " + sendData.length;
                    mLogger.message(msg);
                } catch (IOException ex) {
                    Logger.getLogger(UDPForwarder.class.getName()).log(Level.SEVERE, null, ex);
                }

            }
        } catch (UnsupportedEncodingException ex) {
            Logger.getLogger(UDPForwarder.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    /** This method is invoked when the project starts its execution;
     * This is a good place to put sub-threads or sockets initializations.
     */
    @Override
    public void launch() {

        mLogger.message("Opening UDP socket...") ;

        try {
            //
            // Open a UDP broadcast socket
            mDatagramSocket = new DatagramSocket();
            mDatagramSocket.setBroadcast(true);

            //
            // Enumerate through the interfaces to find all broadcasting addresses.
            //
            Enumeration<NetworkInterface> interfaces = NetworkInterface.getNetworkInterfaces();
            while (interfaces.hasMoreElements()) {

                    NetworkInterface networkInterface = interfaces.nextElement();

//                    if (networkInterface.isLoopback() || !networkInterface.isUp()) {    // TODO test
                    if (!networkInterface.isUp()) {
                        continue; // Don't want to broadcast to inactive inferfaces
                    }

                for (InterfaceAddress interfaceAddress : networkInterface.getInterfaceAddresses()) {

                    System.out.println("---------Internet address: " + interfaceAddress);

                    InetAddress broadcast = interfaceAddress.getBroadcast();
                    if (broadcast == null) {
                        continue;
                    }

//                    System.out.println(PREFIX + broadcast);
                    mBroadcastAddresses.add(broadcast) ;
                }

            }

        } catch (SocketException ex) {
            Logger.getLogger(UDPForwarder.class.getName()).log(Level.SEVERE, null, ex);
        }


    }

    /** This method is executed when the project is stopped;
     * Here you are supposed to stop and join all sub-threads,
     * and close sockets.
     */
    @Override
    public void unload() {
        mBroadcastAddresses.clear();
        mDatagramSocket.close();
        mLogger.message("Socket closed.") ;
    }

    private String toJson(AbstractActivity activity) {

        String json = "{\n";
        if (activity instanceof ActionActivity) {

            ActionActivity aa = (ActionActivity) activity;

            json += "\"atype\": \"action\",";
            json += "\"object\": " + "\"" + aa.getActor() + "\"" + ",";
            json += "\"nameaction\": " + "\"" + aa.getName() + "\"" + ",";

            LinkedList<ActionFeature> a_features = activity.getFeatures();

            for (int i = 0; a_features != null && i < a_features.size(); i++) {

                ActionFeature af = a_features.get(i);
                String val = af.getVal().replace("'", ""); // Values of type string are always enclosed by "'", remove this for json

                json += "\"" + af.getKey() + "\": \"" + val + "\"";
                if (i != a_features.size() - 1) {
                    json += ",";
                }

            }

        } else if (activity instanceof SpeechActivity) {
            SpeechActivity sa = (SpeechActivity) activity;

            json += "\"atype\": \"speech\",";
            json += "\"object\": " + "\"" + sa.getActor() + "\"" + ",";
            json += "\"text\": " + "\"" + sa.getTextOnly("\\UDPFwd=").trim() + "\"";

        } else {
            throw new UnsupportedOperationException("Not supported activity");
        }

        return json + "\n}";
    }

}

<%page args="client_id, display_name, input_output_elements"/>\
\
<?xml version="1.0" encoding="utf-8"?>
<SourceFile Checksum="81CD3EE5B0FDFEA2478685EE480764FB6E16C8E3B5DA74AF2CF40ED16E62CA381B9754536688461BA95599295C52450BD97BFEC7B16664C415491E047647AB88" Timestamp="1DAAA818B5383B3" xmlns="http://www.ni.com/PlatformFramework">
	<SourceModelFeatureSet>
		<ParsableNamespace AssemblyFileVersion="9.12.0.49994" FeatureSetName="Configuration Based Software Core" Name="http://www.ni.com/ConfigurationBasedSoftware.Core" OldestCompatibleVersion="6.3.0.49152" Version="9.8.1.49152" />
		<ParsableNamespace AssemblyFileVersion="9.12.0.49994" FeatureSetName="LabVIEW Controls" Name="http://www.ni.com/Controls.LabVIEW.Design" OldestCompatibleVersion="8.1.0.49152" Version="8.1.0.49152" />
		<ParsableNamespace AssemblyFileVersion="24.3.0.49994" FeatureSetName="InstrumentStudio Measurement UI" Name="http://www.ni.com/InstrumentFramework/ScreenDocument" OldestCompatibleVersion="22.1.0.1" Version="22.1.0.1" />
		<ParsableNamespace AssemblyFileVersion="9.12.0.49994" FeatureSetName="Editor" Name="http://www.ni.com/PanelCommon" OldestCompatibleVersion="6.1.0.0" Version="6.1.0.49152" />
		<ParsableNamespace AssemblyFileVersion="9.12.0.49994" FeatureSetName="Editor" Name="http://www.ni.com/PlatformFramework" OldestCompatibleVersion="8.1.0.49152" Version="8.1.0.49152" />
		<ApplicationVersionInfo Build="24.3.0.49994" Name="Measurement Plug-in UI Editor" Version="24.3.0.49994" />
	</SourceModelFeatureSet>
	<Screen ClientId="${client_id}" DisplayName="${display_name}" Id="20c496a981bb4f73bea9d243756baab5" ServiceClass="ni.examples.SampleMeasurement_Python" xmlns="http://www.ni.com/InstrumentFramework/ScreenDocument">
		<ScreenSurface BackgroundColor="[SMSolidColorBrush]#00ffffff" Height="[float]1000" Id="c47bc3494c0244bab74b59853ae5087f" Left="[float]0" PanelSizeMode="Fixed" Top="[float]0" Width="[float]520" xmlns="http://www.ni.com/ConfigurationBasedSoftware.Core">
        ${input_output_elements}
		</ScreenSurface>
	</Screen>
</SourceFile>
